from django.contrib.auth.models import User
from django.test import TestCase

from NearBeach.models.permission.group import Group
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.user import UserGroup
from NearBeach.utils.api.check_group_list import check_group_list


class CheckGroupListTest(TestCase):
    """The user only needs access to at least one of the requested groups (groups are teams)"""

    def setUp(self):
        self.user = User.objects.create_user(username="group_check_user", password="x")
        self.permission_set = PermissionSet.objects.create(name="group_check_set")
        self.group_a = Group.objects.create(name="group_check_a")
        self.group_b = Group.objects.create(name="group_check_b")
        UserGroup.objects.create(
            username=self.user,
            group=self.group_a,
            permission_set=self.permission_set,
        )

    def test_member_of_all_groups(self):
        self.assertTrue(check_group_list(self.user, [self.group_a]))

    def test_duplicates_are_ignored(self):
        self.assertTrue(check_group_list(self.user, [self.group_a, self.group_a]))

    def test_group_ids_accepted(self):
        self.assertTrue(check_group_list(self.user, [self.group_a.pk]))

    def test_member_of_only_some_groups_is_accepted(self):
        self.assertTrue(check_group_list(self.user, [self.group_a, self.group_b]))

    def test_no_membership_is_rejected(self):
        self.assertFalse(check_group_list(self.user, [self.group_b]))

    def test_empty_list_is_rejected(self):
        self.assertFalse(check_group_list(self.user, []))

    def test_deleted_membership_is_rejected(self):
        UserGroup.objects.update(is_deleted=True)
        self.assertFalse(check_group_list(self.user, [self.group_a]))
