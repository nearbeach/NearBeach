"""/api/v1/user/initial_data/ - the call the app makes on every page load. It tells the frontend who the user is,
what they may do in each group (the permission sets), and the lists the pages are built from."""
from django.contrib.auth.models import User

from NearBeach.models.document.document import Document
from NearBeach.models.misc.tag import Tag
from NearBeach.models.project import ListOfProjectStatus
from NearBeach.models.user import Group, PermissionSet, UserGroup, UserProfilePicture
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

URL = "/api/v1/user/initial_data/"
# The object permission levels of each fixture user: group -> {field: level}
OBJECT_FIELDS = ("customer", "kanban_board", "organisation", "project", "request_for_change", "requirement", "task")
LEVELS = {
    "team_leader": {"QA Team": 4},
    "team_member": {"QA Team": 3},
    "team_intern": {"QA Team": 2},
    "read_only": {"QA Team": 1},
    "read_only_extra": {"QA Team": 1},
    "admin": {"Administration": 4, "QA Team": 4},
    "dark_admin": {"Administration": 4},
    "no_group": {},
}


class UserInitialDataTests(BaseApiClass):
    def _get(self, username=None):
        # force_login: a user in no group can not log in through the api, but can still hold a session
        self.client.logout()
        if username is not None:
            self.client.force_login(User.objects.get(username=username))

        return self.client.get(URL)

    def _permissions(self, username):
        response = self._get(username)
        self.assertEqual(response.status_code, 200, username)
        return {row["group_name"]: row for row in response.data["permissions"]}

    # ---------- who can ask ----------
    def test_anonymous_users_are_refused(self):
        self.assertEqual(self._get().status_code, 403)

    def test_every_fixture_user_can_load_it(self):
        for username in LEVELS:
            with self.subTest(username=username):
                self.assertEqual(self._get(username).status_code, 200)

    # ---------- the user ----------
    def test_users_are_told_about_themselves_only(self):
        for username in ("team_member", "read_only", "admin"):
            with self.subTest(username=username):
                data = self._get(username).data
                user = User.objects.get(username=username)

                self.assertEqual(data["id"], user.pk)
                self.assertEqual(data["username"], username)
                self.assertEqual(data["email"], user.email)
                self.assertEqual(data["full_name"], f"{user.first_name} {user.last_name}")

    def test_the_response_never_contains_password_data(self):
        data = self._get("team_member").data

        self.assertNotIn("password", data)
        self.assertEqual(
            set(data),
            {
                "id", "username", "first_name", "last_name", "full_name", "email", "profile_picture",
                "profile_picture_path", "all_groups", "permissions", "object_status", "object_types", "tags",
            },
        )

    def test_a_user_without_a_picture_has_null_picture_fields(self):
        data = self._get("team_member").data

        self.assertIsNone(data["profile_picture"])
        self.assertIsNone(data["profile_picture_path"])

    def test_a_user_with_a_picture_gets_its_key_and_path(self):
        """The call every page makes used to crash (a 500) for anyone with a profile picture"""
        user = User.objects.get(username="team_member")
        picture = Document.objects.create(
            change_user=user,
            creation_user=user,
            description="Me",
            url_location="https://example.org/me.png",
            upload_successfully=True,
        )
        UserProfilePicture.objects.create(username=user, document=picture, change_user=user, creation_user=user)

        response = self._get("team_member")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data["profile_picture"]), str(picture.key))
        self.assertEqual(response.data["profile_picture_path"], f"/private/{picture.key}")

    # ---------- permissions ----------
    def test_each_user_gets_their_groups_and_levels(self):
        for username, expected in LEVELS.items():
            with self.subTest(username=username):
                permissions = self._permissions(username)

                self.assertEqual(set(permissions), set(expected))
                for group, level in expected.items():
                    for field in OBJECT_FIELDS:
                        self.assertEqual(permissions[group][field], level, (group, field))

    def test_only_admins_get_administration_permissions(self):
        for username in ("team_leader", "team_member", "read_only", "no_group"):
            with self.subTest(username=username):
                for row in self._permissions(username).values():
                    self.assertEqual(
                        [row[field] for field in row if field.startswith("administration_")], [0, 0, 0, 0]
                    )

        for row in self._permissions("admin").values():
            self.assertEqual([row[field] for field in row if field.startswith("administration_")], [4, 4, 4, 4])

    def test_additive_note_and_document_permissions(self):
        extra = self._permissions("read_only_extra")["QA Team"]
        plain = self._permissions("read_only")["QA Team"]
        additive = ("document", "kanban_note", "organisation_note", "project_note", "requirement_item_note",
                    "requirement_note", "task_note")

        for field in additive:
            with self.subTest(field=field):
                self.assertEqual(extra[field], 1)
                self.assertEqual(plain[field], 0)

    def test_a_user_in_no_group_has_no_permissions(self):
        self.assertEqual(self._get("no_group").data["permissions"], [])

    def test_a_user_in_two_groups_gets_a_row_for_each(self):
        rows = self._get("admin").data["permissions"]

        self.assertEqual(sorted(row["group_name"] for row in rows), ["Administration", "QA Team"])
        self.assertEqual(sorted(row["group_id"] for row in rows), [1, 2])

    def test_removed_memberships_do_not_count(self):
        UserGroup.objects.filter(username__username="team_member").update(is_deleted=True)

        self.assertEqual(self._get("team_member").data["permissions"], [])

    def test_deleted_groups_and_permission_sets_do_not_count(self):
        Group.objects.filter(name="QA Team").update(is_deleted=True)
        self.assertEqual(self._get("team_member").data["permissions"], [])

        Group.objects.filter(name="QA Team").update(is_deleted=False)
        PermissionSet.objects.filter(name="Add and Edit").update(is_deleted=True)
        self.assertEqual(self._get("team_member").data["permissions"], [])

    def test_changing_a_permission_set_changes_the_answer(self):
        PermissionSet.objects.filter(name="Add and Edit").update(project=1)

        self.assertEqual(self._permissions("team_member")["QA Team"]["project"], 1)

    # ---------- the lists the pages are built from ----------
    def test_all_groups_are_listed_by_name(self):
        data = self._get("team_member").data

        self.assertEqual([group["name"] for group in data["all_groups"]],
                         ["Administration", "Empty Group", "No Group", "QA Team"])

    def test_deleted_groups_are_not_listed(self):
        Group.objects.filter(name="Empty Group").update(is_deleted=True)

        names = [group["name"] for group in self._get("team_member").data["all_groups"]]

        self.assertNotIn("Empty Group", names)

    def test_object_statuses_are_listed_in_order(self):
        statuses = self._get("team_member").data["object_status"]

        self.assertEqual(set(statuses), {"requirement", "requirement_item", "project", "task"})
        expected = list(
            ListOfProjectStatus.objects.filter(is_deleted=False).order_by("sort_order").values_list("pk", flat=True)
        )
        self.assertEqual([row["id"] for row in statuses["project"]], expected)

    def test_deleted_statuses_are_not_listed(self):
        first = ListOfProjectStatus.objects.filter(is_deleted=False).order_by("sort_order").first()
        ListOfProjectStatus.objects.filter(pk=first.pk).update(is_deleted=True)

        ids = [row["id"] for row in self._get("team_member").data["object_status"]["project"]]

        self.assertNotIn(first.pk, ids)

    def test_object_types_are_listed(self):
        types = self._get("team_member").data["object_types"]

        self.assertEqual(set(types), {"requirement", "requirement_item"})
        self.assertGreater(len(types["requirement"]), 0)
        self.assertGreater(len(types["requirement_item"]), 0)

    def test_tags_are_listed_by_name_and_deleted_ones_are_not(self):
        Tag.objects.filter(pk=Tag.objects.order_by("name").first().pk).update(is_deleted=True)

        names = [tag["name"] for tag in self._get("team_member").data["tags"]]

        self.assertEqual(names, sorted(names))
        self.assertEqual(len(names), Tag.objects.filter(is_deleted=False).count())
