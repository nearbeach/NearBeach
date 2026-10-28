"""The two decorators every project api method sits behind, called directly with stand-in requests so every branch
(not just the ones the project routes happen to reach) is checked."""
from types import SimpleNamespace

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import NotFound, PermissionDenied

from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.user import Group, PermissionSet, UserGroup


def view_returning_the_level(request, *args, **kwargs):
    return kwargs["user_level"]


class DecoratorTestBase(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def request(self, path, username="team_member"):
        return SimpleNamespace(path=path, user=User.objects.get(username=username))


class ObjectPermissionTests(DecoratorTestBase):
    def call(self, path, username="team_member", minimum=1, **decorator_kwargs):
        view = object_permission(minimum, **decorator_kwargs)(view_returning_the_level)
        return view(self.request(path, username))

    def test_the_view_is_given_the_users_level(self):
        self.assertEqual(self.call("/api/v1/project/2/", "team_member"), 3)
        self.assertEqual(self.call("/api/v1/project/2/", "read_only"), 1)

    def test_the_level_has_to_be_enough(self):
        self.assertEqual(self.call("/api/v1/project/2/", "team_member", minimum=3), 3)
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/2/", "team_member", minimum=4)

    def test_sub_resources_use_the_object_in_the_path(self):
        self.assertEqual(self.call("/api/v1/project/2/notes/5/", "team_member"), 3)

    def test_an_object_in_another_group_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/1/", "team_member")

    def test_a_user_in_no_group_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/2/", "no_group")

    def test_an_object_that_does_not_exist_is_not_found(self):
        with self.assertRaises(NotFound):
            self.call("/api/v1/project/99999/")

    def test_a_deleted_object_is_not_found(self):
        from NearBeach.models.project import Project

        Project.objects.filter(pk=2).update(is_deleted=True)

        with self.assertRaises(NotFound):
            self.call("/api/v1/project/2/")

    def test_an_id_that_is_not_a_number_is_not_found(self):
        for bad_id in ("abc", "1.5", "-1", "2abc"):
            with self.subTest(bad_id=bad_id), self.assertRaises(NotFound):
                self.call(f"/api/v1/project/{bad_id}/")

    def test_an_unknown_kind_of_object_is_not_found(self):
        with self.assertRaises(NotFound):
            self.call("/api/v1/banana/2/")

    def test_a_path_with_no_object_in_it_is_refused(self):
        for path in ("/api/v1/project/", "/api/v1/", "/"):
            with self.subTest(path=path), self.assertRaises(PermissionDenied):
                self.call(path)

    def test_a_removed_group_membership_is_refused(self):
        UserGroup.objects.filter(username__username="team_member").update(is_deleted=True)

        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/2/")

    def test_a_request_can_be_the_drf_request_wrapper(self):
        """In a viewset the first argument is the view (self) and the request is inside it"""
        view = object_permission(1)(lambda self, request, *args, **kwargs: kwargs["user_level"])
        wrapper = SimpleNamespace(request=self.request("/api/v1/project/2/"))

        self.assertEqual(view(wrapper, None), 3)

    # ---------- child objects are reached through their parent ----------
    def test_a_child_object_uses_its_parents_groups(self):
        item = RequirementItem.objects.get(pk=2)  # its requirement is in the QA group

        self.assertEqual(self.call(f"/api/v1/requirement_item/{item.pk}/", "team_member"), 3)

    def test_a_child_object_in_another_groups_parent_is_refused(self):
        item = RequirementItem.objects.get(pk=1)  # its requirement is Administration only

        with self.assertRaises(PermissionDenied):
            self.call(f"/api/v1/requirement_item/{item.pk}/", "team_member")

    def test_a_child_that_does_not_exist_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/requirement_item/99999/")


class AdditivePermissionTests(DecoratorTestBase):
    """read_only_extra has project=1 and project_note=1 in one permission set; read_only has no extras"""

    def call(self, username, additive_permission="project_note", minimum=2, path="/api/v1/project/2/"):
        view = object_permission(minimum, additive_permission=additive_permission)(view_returning_the_level)
        return view(self.request(path, username))

    def test_a_read_only_user_with_the_extra_permission_is_let_in(self):
        self.assertEqual(self.call("read_only_extra"), 1)

    def test_a_read_only_user_without_it_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("read_only")

    def test_it_is_only_for_the_permission_named(self):
        PermissionSet.objects.filter(name="Read Only + Extra").update(task_note=1, project_note=0)

        with self.assertRaises(PermissionDenied):
            self.call("read_only_extra", additive_permission="project_note")
        self.assertEqual(self.call("read_only_extra", additive_permission="task_note"), 1)

    def test_it_does_not_replace_being_able_to_read(self):
        PermissionSet.objects.filter(name="Read Only + Extra").update(project=0)

        with self.assertRaises(PermissionDenied):
            self.call("read_only_extra")

    def test_it_does_not_lower_the_level_for_users_who_already_have_enough(self):
        self.assertEqual(self.call("team_member"), 3)

    def test_a_deleted_permission_set_gives_nothing(self):
        PermissionSet.objects.filter(name="Read Only + Extra").update(is_deleted=True)

        with self.assertRaises(PermissionDenied):
            self.call("read_only_extra")

    def test_it_only_applies_on_objects_the_users_group_is_assigned_to(self):
        with self.assertRaises(PermissionDenied):
            self.call("read_only_extra", path="/api/v1/project/1/")

    def test_an_extra_permission_in_another_permission_set_does_not_count(self):
        admin = User.objects.get(username="admin")
        extra_only = PermissionSet.objects.create(
            name="Notes only", project=0, project_note=1, creation_user=admin, change_user=admin
        )
        group = Group.objects.get(name="Empty Group")
        ObjectAssignment.objects.create(project_id=2, group=group, creation_user=admin, change_user=admin)
        UserGroup.objects.create(
            username=User.objects.get(username="read_only"), group=group, permission_set=extra_only,
            creation_user=admin, change_user=admin,
        )

        with self.assertRaises(PermissionDenied):
            self.call("read_only")


class DestinationPermissionTests(DecoratorTestBase):
    """For routes with no object id (list, create): the level is the user's highest in any group"""

    def call(self, path, username="team_member", minimum=1):
        view = destination_permission(minimum)(view_returning_the_level)
        return view(self.request(path, username))

    def test_the_view_is_given_the_highest_level(self):
        self.assertEqual(self.call("/api/v1/project/", "team_member"), 3)
        self.assertEqual(self.call("/api/v1/project/", "admin"), 4)

    def test_the_level_has_to_be_enough(self):
        self.assertEqual(self.call("/api/v1/project/", "team_member", minimum=3), 3)
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/", "team_intern", minimum=3)

    def test_a_user_in_no_group_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/", "no_group")

    def test_an_unknown_kind_of_object_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/banana/")

    def test_a_path_with_no_destination_is_refused(self):
        for path in ("/", "/api/", "/api/v1"):
            with self.subTest(path=path), self.assertRaises(PermissionDenied):
                self.call(path)

    def test_a_child_object_type_uses_its_parents_permission(self):
        """requirement_item is checked against the requirement permission"""
        self.assertEqual(self.call("/api/v1/requirement_item/", "team_leader"), 4)

    def test_a_removed_group_membership_is_refused(self):
        UserGroup.objects.filter(username__username="team_member").update(is_deleted=True)

        with self.assertRaises(PermissionDenied):
            self.call("/api/v1/project/")

    def test_a_request_can_be_the_drf_request_wrapper(self):
        view = destination_permission(1)(lambda self, request, *args, **kwargs: kwargs["user_level"])
        wrapper = SimpleNamespace(request=self.request("/api/v1/project/"))

        self.assertEqual(view(wrapper, None), 3)
