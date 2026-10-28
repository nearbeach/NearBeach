"""CRUD tests for the groups and users of a project, run as the team leader.

Project 2 ("Project - QA Team") is in the QA Team group (2). In the fixture:
 - users assigned to it: read_only (5) and team_leader (2)
 - members of the QA Team: admin (1), team_leader (2), team_member (3), team_intern (4), read_only (5), read_only_extra (8)
 - Administration (1) has admin (1) and dark_admin (7); groups 3 and 4 have no members
"""

from django.contrib.auth import get_user_model

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.tests.tests_api.tests_crud.test_team_leader.test_crud_project import (
    ADMIN_GROUP,
    EMPTY_GROUP,
    QA_GROUP,
    QA_PROJECT_URL,
    TeamLeaderProjectBase,
)

GROUPS_URL = f"{QA_PROJECT_URL}groups/"
USERS_URL = f"{QA_PROJECT_URL}users/"

READ_ONLY, TEAM_LEADER, TEAM_MEMBER, TEAM_INTERN = 5, 2, 3, 4
ADMIN_USER, DARK_ADMIN, READ_ONLY_EXTRA = 1, 7, 8


class GroupsAndUsersBase(TeamLeaderProjectBase):
    def _lists(self):
        """Ids in each list of the groups endpoint"""
        data = self.client.get(GROUPS_URL).data
        return {key: sorted(item["id"] for item in data[key]) for key in ("group_list", "user_list", "potential_user_list")}

    def _group_rows(self, group_id, project_id=2):
        return ObjectAssignment.objects.filter(project_id=project_id, group_id=group_id)

    def _user_rows(self, user_id, project_id=2):
        return ObjectAssignment.objects.filter(project_id=project_id, assigned_user_id=user_id)


class ProjectGroupListTests(GroupsAndUsersBase):
    def test_list_has_the_groups_and_users_of_the_project(self):
        response = self.client.get(GROUPS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"group_list", "user_list", "potential_user_list"})
        self.assertEqual(
            self._lists(),
            {
                "group_list": [QA_GROUP],
                "user_list": [TEAM_LEADER, READ_ONLY],
                "potential_user_list": [ADMIN_USER, TEAM_MEMBER, TEAM_INTERN, READ_ONLY_EXTRA],
            },
        )

    def test_group_rows_have_an_id_and_name(self):
        group = self.client.get(GROUPS_URL).data["group_list"][0]

        self.assertEqual(group["id"], QA_GROUP)
        self.assertIn("name", group)
        self.assertIn("parent_group", group)

    def test_user_rows_have_a_full_name(self):
        users = {user["id"]: user for user in self.client.get(GROUPS_URL).data["user_list"]}

        self.assertEqual(users[TEAM_LEADER]["full_name"], "Team Leader")
        self.assertEqual(users[READ_ONLY]["full_name"], "Read Only")

    def test_a_deleted_group_assignment_is_not_listed(self):
        # The fixture has a deleted QA Team assignment on the project - it must not show twice
        self.assertEqual(self._lists()["group_list"], [QA_GROUP])

    def test_inactive_users_are_not_listed(self):
        get_user_model().objects.filter(pk=READ_ONLY).update(is_active=False)

        lists = self._lists()
        self.assertNotIn(READ_ONLY, lists["user_list"])
        self.assertNotIn(READ_ONLY, lists["potential_user_list"])

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/groups/").status_code, 404)


class ProjectGroupAddTests(GroupsAndUsersBase):
    def _add(self, *groups):
        return self.client.post(GROUPS_URL, {"group_list": list(groups)}, format="json")

    def test_adding_a_group_returns_the_new_list(self):
        response = self._add(EMPTY_GROUP)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(sorted(g["id"] for g in response.data["group_list"]), [QA_GROUP, EMPTY_GROUP])

    def test_adding_a_group_saves_the_assignment(self):
        self._add(EMPTY_GROUP)

        row = self._group_rows(EMPTY_GROUP).get()
        self.assertFalse(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_adding_several_groups_at_once(self):
        response = self._add(EMPTY_GROUP, ADMIN_GROUP)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(self._lists()["group_list"], [ADMIN_GROUP, QA_GROUP, EMPTY_GROUP])

    def test_adding_a_group_makes_its_members_potential_users(self):
        self.assertNotIn(DARK_ADMIN, self._lists()["potential_user_list"])

        self._add(ADMIN_GROUP)

        self.assertIn(DARK_ADMIN, self._lists()["potential_user_list"])

    def test_adding_the_same_group_twice_keeps_one_row(self):
        self._add(EMPTY_GROUP)
        response = self._add(EMPTY_GROUP)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self._group_rows(EMPTY_GROUP, ).filter(is_deleted=False).count(), 1)

    def test_adding_does_not_touch_other_projects(self):
        before = ObjectAssignment.objects.filter(project_id=1).count()

        self._add(EMPTY_GROUP)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=1).count(), before)

    def test_bad_group_lists_are_rejected_and_change_nothing(self):
        bodies = {
            "empty list": {"group_list": []},
            "missing list": {},
            "unknown group": {"group_list": [9999]},
            "not a number": {"group_list": ["abc"]},
            "not a list": {"group_list": 3},
        }
        before = ObjectAssignment.objects.filter(project_id=2).count()

        for name, body in bodies.items():
            with self.subTest(name):
                response = self.client.post(GROUPS_URL, body, format="json")
                self.assertEqual(response.status_code, 400, response.data)
                self.assertIn("group_list", response.data)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=2).count(), before)

    def test_a_deleted_group_cannot_be_added(self):
        from NearBeach.models.user import Group

        Group.objects.filter(pk=EMPTY_GROUP).update(is_deleted=True)

        self.assertEqual(self._add(EMPTY_GROUP).status_code, 400)
        self.assertFalse(self._group_rows(EMPTY_GROUP).exists())

    def test_a_removed_group_can_be_added_again(self):
        self._add(EMPTY_GROUP)
        self.client.delete(f"{GROUPS_URL}{EMPTY_GROUP}/")

        response = self._add(EMPTY_GROUP)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self._lists()["group_list"], [QA_GROUP, EMPTY_GROUP])

    def test_missing_project_is_not_found(self):
        response = self.client.post("/api/v1/project/9999/groups/", {"group_list": [EMPTY_GROUP]}, format="json")

        self.assertEqual(response.status_code, 404)


class ProjectGroupRemoveTests(GroupsAndUsersBase):
    def setUp(self):
        super().setUp()
        # A second group so there is one that can be removed
        self.client.post(GROUPS_URL, {"group_list": [EMPTY_GROUP]}, format="json")

    def test_removing_a_group_returns_the_new_list(self):
        response = self.client.delete(f"{GROUPS_URL}{EMPTY_GROUP}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([g["id"] for g in response.data["group_list"]], [QA_GROUP])

    def test_removing_a_group_is_a_soft_delete(self):
        self.client.delete(f"{GROUPS_URL}{EMPTY_GROUP}/")

        row = self._group_rows(EMPTY_GROUP).get()
        self.assertTrue(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_removing_a_group_leaves_the_others(self):
        self.client.delete(f"{GROUPS_URL}{EMPTY_GROUP}/")

        self.assertTrue(self._group_rows(QA_GROUP).filter(is_deleted=False).exists())

    def test_the_last_group_cannot_be_removed(self):
        """Regression - GroupService.delete used to count every assignment on the project (users included), not only
        groups. Project 2 has two users assigned, so its only group could be removed and the project left with no group.
        """
        self.client.delete(f"{GROUPS_URL}{EMPTY_GROUP}/")

        response = self.client.delete(f"{GROUPS_URL}{QA_GROUP}/")

        self.assertEqual(response.status_code, 400)
        self.assertTrue(self._group_rows(QA_GROUP).filter(is_deleted=False).exists())

    def test_the_last_group_cannot_be_removed_from_a_project_without_users(self):
        project = self._make_project("No users")
        url = f"/api/v1/project/{project.pk}/groups/{QA_GROUP}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(self._group_rows(QA_GROUP, project.pk).filter(is_deleted=False).exists())

    def test_a_group_that_is_not_on_the_project_cannot_be_removed(self):
        response = self.client.delete(f"{GROUPS_URL}{ADMIN_GROUP}/")

        self.assertEqual(response.status_code, 400)

    def test_removing_a_group_removes_users_that_only_came_from_it(self):
        # dark_admin is only in Administration - so only that group gives them access
        self.client.post(GROUPS_URL, {"group_list": [ADMIN_GROUP]}, format="json")
        self.client.post(USERS_URL, {"user_list": [DARK_ADMIN, TEAM_MEMBER]}, format="json")

        self.client.delete(f"{GROUPS_URL}{ADMIN_GROUP}/")

        self.assertTrue(self._user_rows(DARK_ADMIN).get().is_deleted)
        # team_member is also in the QA Team, so keeps their place
        self.assertFalse(self._user_rows(TEAM_MEMBER).get().is_deleted)
        self.assertEqual(self._lists()["user_list"], [TEAM_LEADER, TEAM_MEMBER, READ_ONLY])

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete(f"/api/v1/project/9999/groups/{EMPTY_GROUP}/").status_code, 404)


class ProjectUserAddTests(GroupsAndUsersBase):
    def _add(self, *users):
        return self.client.post(USERS_URL, {"user_list": list(users)}, format="json")

    def test_adding_a_user(self):
        response = self._add(TEAM_MEMBER)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data, {})

    def test_adding_a_user_saves_the_assignment(self):
        self._add(TEAM_MEMBER)

        row = self._user_rows(TEAM_MEMBER).get()
        self.assertFalse(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_an_added_user_moves_from_potential_to_assigned(self):
        self._add(TEAM_MEMBER)

        lists = self._lists()
        self.assertIn(TEAM_MEMBER, lists["user_list"])
        self.assertNotIn(TEAM_MEMBER, lists["potential_user_list"])

    def test_adding_several_users_at_once(self):
        self._add(TEAM_MEMBER, TEAM_INTERN)

        self.assertEqual(self._lists()["user_list"], [TEAM_LEADER, TEAM_MEMBER, TEAM_INTERN, READ_ONLY])

    def test_adding_the_same_user_twice_keeps_one_row(self):
        self._add(TEAM_MEMBER)
        self.assertEqual(self._add(TEAM_MEMBER).status_code, 201)

        self.assertEqual(self._user_rows(TEAM_MEMBER).filter(is_deleted=False).count(), 1)

    def test_a_user_already_on_the_project_is_not_added_again(self):
        self._add(READ_ONLY)

        self.assertEqual(self._user_rows(READ_ONLY).filter(is_deleted=False).count(), 1)

    def test_bad_user_lists_are_rejected_and_change_nothing(self):
        bodies = {
            "empty list": {"user_list": []},
            "missing list": {},
            "unknown user": {"user_list": [9999]},
            "not a number": {"user_list": ["abc"]},
        }
        before = ObjectAssignment.objects.filter(project_id=2).count()

        for name, body in bodies.items():
            with self.subTest(name):
                response = self.client.post(USERS_URL, body, format="json")
                self.assertEqual(response.status_code, 400, response.data)
                self.assertIn("user_list", response.data)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=2).count(), before)

    def test_an_inactive_user_cannot_be_added(self):
        get_user_model().objects.filter(pk=TEAM_MEMBER).update(is_active=False)

        self.assertEqual(self._add(TEAM_MEMBER).status_code, 400)
        self.assertFalse(self._user_rows(TEAM_MEMBER).exists())

    def test_a_removed_user_can_be_added_again(self):
        self._add(TEAM_MEMBER)
        self.client.delete(f"{USERS_URL}{TEAM_MEMBER}/")

        self.assertEqual(self._add(TEAM_MEMBER).status_code, 201)
        self.assertEqual(self._user_rows(TEAM_MEMBER).filter(is_deleted=False).count(), 1)

    def test_missing_project_is_not_found(self):
        response = self.client.post("/api/v1/project/9999/users/", {"user_list": [TEAM_MEMBER]}, format="json")

        self.assertEqual(response.status_code, 404)


class ProjectUserRemoveTests(GroupsAndUsersBase):
    def test_removing_a_user(self):
        response = self.client.delete(f"{USERS_URL}{READ_ONLY}/")

        self.assertEqual(response.status_code, 204)

    def test_removing_a_user_is_a_soft_delete(self):
        self.client.delete(f"{USERS_URL}{READ_ONLY}/")

        row = self._user_rows(READ_ONLY).get()
        self.assertTrue(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_a_removed_user_goes_back_to_potential(self):
        self.client.delete(f"{USERS_URL}{READ_ONLY}/")

        lists = self._lists()
        self.assertEqual(lists["user_list"], [TEAM_LEADER])
        self.assertIn(READ_ONLY, lists["potential_user_list"])

    def test_removing_a_user_leaves_the_others_and_the_groups(self):
        self.client.delete(f"{USERS_URL}{READ_ONLY}/")

        self.assertFalse(self._user_rows(TEAM_LEADER).get().is_deleted)
        self.assertEqual(self._lists()["group_list"], [QA_GROUP])

    def test_removing_a_user_does_not_touch_other_projects(self):
        # admin (1) is on project 1
        self.client.delete(f"{USERS_URL}{ADMIN_USER}/")

        self.assertFalse(self._user_rows(ADMIN_USER, project_id=1).get().is_deleted)

    def test_a_user_that_is_not_on_the_project_cannot_be_removed(self):
        self.assertEqual(self.client.delete(f"{USERS_URL}{TEAM_MEMBER}/").status_code, 400)

    def test_removing_a_user_twice_is_still_accepted(self):
        """The service does not look at is_deleted, so a second remove finds the old row"""
        self.client.delete(f"{USERS_URL}{READ_ONLY}/")

        self.assertEqual(self.client.delete(f"{USERS_URL}{READ_ONLY}/").status_code, 204)

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete(f"/api/v1/project/9999/users/{READ_ONLY}/").status_code, 404)
