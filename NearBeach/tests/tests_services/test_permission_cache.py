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
