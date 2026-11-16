from django.contrib.auth.models import User
from django.test import override_settings
from django.utils import timezone

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.user import UserGroup
from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.permission_cache import get_destination_permission, get_object_permission


class PermissionCacheTests(BaseApiClass):
    """The permission decorators cache their lookups - the cache must never outlive a permission change"""
    username = "read_only"
    password = "Test1234$"

    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username="read_only")

    def test_object_lookup_is_cached(self):
        """Test - the second lookup for the same user and object does not touch the database"""
        first = get_object_permission(self.user, "project", 2)
        with self.assertNumQueries(0):
            second = get_object_permission(self.user, "project", 2)
        self.assertEqual(first, second)
        self.assertEqual(first[0], 1)

    def test_destination_lookup_is_cached(self):
        """Test - the second destination lookup does not touch the database"""
        first = get_destination_permission(self.user, "project")
        with self.assertNumQueries(0):
            second = get_destination_permission(self.user, "project")
        self.assertEqual(first, second)

    @override_settings(PERMISSION_CACHE_TTL=0)
    def test_cache_can_be_switched_off(self):
        """Test - a timeout of 0 sends every lookup to the database"""
        get_object_permission(self.user, "project", 2)
        with self.assertNumQueries(1):
            get_object_permission(self.user, "project", 2)

    def test_soft_deleting_user_group_takes_effect_at_once(self):
        """Test - soft deleting with update() (which fires no signal) removes access straight away"""
        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 200)

        UserGroup.objects.filter(username=self.user).update(is_deleted=True, date_modified=timezone.now())

        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 403)

    def test_removing_group_access_from_object_takes_effect_at_once(self):
        """Test - soft deleting the group's access row on the object removes access straight away"""
        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 200)

        ObjectAssignment.objects.filter(
            project_id=2,
            group_id__isnull=False,
        ).update(is_deleted=True, date_modified=timezone.now())

        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 403)

    def test_changing_permission_set_level_takes_effect_at_once(self):
        """Test - raising the permission set level is seen by the next request"""
        self.assertEqual(get_object_permission(self.user, "project", 2)[0], 1)

        permission_set_ids = UserGroup.objects.filter(username=self.user, is_deleted=False).values("permission_set_id")
        for permission_set in PermissionSet.objects.filter(id__in=permission_set_ids):
            permission_set.project = 4
            permission_set.save()

        self.assertEqual(get_object_permission(self.user, "project", 2)[0], 4)

    def test_denied_result_is_cached_then_cleared_on_grant(self):
        """Test - a cached "no access" is replaced once the user is given a group"""
        UserGroup.objects.filter(username=self.user).update(is_deleted=True)
        self.assertIsNone(get_object_permission(self.user, "project", 2)[0])
        with self.assertNumQueries(0):
            self.assertIsNone(get_object_permission(self.user, "project", 2)[0])

        UserGroup.objects.filter(username=self.user).update(is_deleted=False)

        self.assertEqual(get_object_permission(self.user, "project", 2)[0], 1)

    def test_deleted_object_still_not_found(self):
        """Test - the object existence check stays live, so a soft deleted object 404s even with a warm cache"""
        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 200)

        from NearBeach.models.project import Project
        Project.objects.filter(pk=2).update(is_deleted=True)

        self.assertEqual(self.client.get("/api/v1/project/2/").status_code, 404)


class PermissionCacheInvalidationTests(BaseApiClass):
    """Exercise the model managers and signals against previously cached answers."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username="read_only")

    def assert_cached_level(self, expected):
        self.assertEqual(get_object_permission(self.user, "project", 2), (expected, False))
        self.assertEqual(get_destination_permission(self.user, "project"), expected)
        with self.assertNumQueries(0):
            self.assertEqual(get_object_permission(self.user, "project", 2), (expected, False))
            self.assertEqual(get_destination_permission(self.user, "project"), expected)

    def test_membership_save_revokes_cached_object_and_destination_access(self):
        self.assert_cached_level(1)
        for membership in UserGroup.objects.filter(username=self.user):
            membership.is_deleted = True
            membership.save()
        self.assert_cached_level(None)

    def test_membership_delete_revokes_cached_object_and_destination_access(self):
        self.assert_cached_level(1)
        for membership in UserGroup.objects.filter(username=self.user):
            membership.delete()
        self.assert_cached_level(None)

    def test_bulk_create_membership_replaces_cached_denial(self):
        memberships = list(UserGroup.objects.filter(username=self.user))
        for membership in memberships:
            membership.delete()
            membership.pk = None
        self.assert_cached_level(None)
        created = UserGroup.objects.bulk_create(memberships)
        self.assertEqual(len(created), len(memberships))
        self.assert_cached_level(1)

    def test_bulk_update_permission_set_revokes_cached_grant(self):
        self.assert_cached_level(1)
        permissions = list(PermissionSet.objects.filter(
            id__in=UserGroup.objects.filter(username=self.user).values("permission_set_id")
        ))
        for permission in permissions:
            permission.project = 0
        self.assertEqual(PermissionSet.objects.bulk_update(permissions, ["project"]), len(permissions))
        self.assert_cached_level(0)

    def test_queryset_delete_membership_revokes_cached_grant(self):
        self.assert_cached_level(1)
        deleted, _ = UserGroup.objects.filter(username=self.user).delete()
        self.assertGreater(deleted, 0)
        self.assert_cached_level(None)

    def test_group_assignment_save_and_delete_invalidate_object_access(self):
        assignments = list(ObjectAssignment.objects.filter(project_id=2, group_id__isnull=False))
        self.assertEqual(get_object_permission(self.user, "project", 2)[0], 1)
        for assignment in assignments:
            assignment.is_deleted = True
            assignment.save()
        self.assertIsNone(get_object_permission(self.user, "project", 2)[0])
        for assignment in assignments:
            assignment.is_deleted = False
            assignment.save()
        self.assertEqual(get_object_permission(self.user, "project", 2)[0], 1)
        for assignment in assignments:
            assignment.delete()
        self.assertIsNone(get_object_permission(self.user, "project", 2)[0])

    def test_organisation_permission_does_not_require_object_group_assignment(self):
        ObjectAssignment.objects.filter(group_id__isnull=False).delete()
        self.assertEqual(get_object_permission(self.user, "organisation", 1)[0], 1)
        with self.assertNumQueries(0):
            self.assertEqual(get_object_permission(self.user, "organisation", 1)[0], 1)

    def test_additive_grant_is_invalidated_when_permission_is_revoked(self):
        user = User.objects.get(username="read_only_extra")
        self.assertEqual(get_object_permission(user, "project", 2, "project_note"), (1, True))
        PermissionSet.objects.filter(
            id__in=UserGroup.objects.filter(username=user).values("permission_set_id")
        ).update(project_note=0)
        self.assertEqual(get_object_permission(user, "project", 2, "project_note"), (1, False))
