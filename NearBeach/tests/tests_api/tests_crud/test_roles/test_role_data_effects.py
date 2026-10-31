"""What every role can really DO to the QA project's data.

The permission tests (tests_permissions) check status codes, and test_team_leader checks the data for one role. These
check the one thing that matters for every role: a request that is refused changes nothing, and a request that is
allowed changes the data and gets the documented answer.

Each operation is run as each role inside its own rolled-back transaction, with a snapshot of the affected tables taken
before and after.

Fixture roles (project 2 "Project - QA Team" belongs to group 2 only; project 1 to group 1 only):
  admin / team_leader : full permission (4)   team_member : add and edit (3)   team_intern : edit only (2)
  read_only, read_only_extra : read only (1)  no_group : not in a group          dark_admin : level 4, group 1 only
"""
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.test import APIClient

from django.test import TestCase

from NearBeach.models.customer import Customer
from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.document.folder import Folder
from NearBeach.models.misc.misc import PublicLink
from NearBeach.models.misc.note import ObjectNote
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.organisation import Organisation
from NearBeach.models.project import Project
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.models.user import Group, PermissionSet, UserGroup

PROJECT = "/api/v1/project/2/"
TABLES = (Project, ObjectAssignment, ObjectNote, PublicLink, Document, DocumentPermission, Folder, Sprint,
          Customer, Organisation)

# role -> permission level on project 2 (None = cannot reach it at all)
LEVEL_ON_QA_PROJECT = {
    "admin": 4,
    "team_leader": 4,
    "team_member": 3,
    "team_intern": 2,
    "read_only": 1,
    "read_only_extra": 1,
    "dark_admin": None,
    "no_group": None,
}
# role -> highest level in any group (what creating a project needs) and the groups they can create in
LEVEL_ANYWHERE = {**LEVEL_ON_QA_PROJECT, "dark_admin": 4}
CREATE_IN = {**{role: [2] for role in LEVEL_ON_QA_PROJECT}, "admin": [1, 2], "dark_admin": [1]}

# name, method, url, body, level needed, status when allowed, whether it changes data
OPERATIONS = [
    ("read the project", "GET", PROJECT, None, 1, 200, False),
    ("list the notes", "GET", f"{PROJECT}notes/", None, 1, 200, False),
    ("list the documents", "GET", f"{PROJECT}documents/", None, 1, 200, False),
    ("list the groups", "GET", f"{PROJECT}groups/", None, 1, 200, False),
    ("update the project", "PATCH", PROJECT, {"title": "Renamed"}, 2, 200, True),
    ("add a note", "POST", f"{PROJECT}notes/", {"note": "A note"}, 2, 201, True),
    ("add a public link", "POST", f"{PROJECT}public_link/", None, 2, 201, True),
    ("add a link", "POST", f"{PROJECT}link_list/",
     {"object_type": "task", "object_id": 2, "object_relation": "relates"}, 2, 201, True),
    ("add a sprint", "POST", f"{PROJECT}sprint/",
     {"title": "S", "start_date": "2026-01-01T00:00:00Z", "end_date": "2026-02-01T00:00:00Z"}, 2, 201, True),
    ("add a folder", "POST", f"{PROJECT}documents/", {"type": "folder", "description": "F"}, 2, 201, True),
    ("add a group", "POST", f"{PROJECT}groups/", {"group_list": [3]}, 2, 201, True),
    ("add a user", "POST", f"{PROJECT}users/", {"user_list": [7]}, 2, 201, True),
    ("link a customer", "POST", f"{PROJECT}customer/", {"id": 1}, 2, 201, True),
    # The fixture project already has organisation 1, so linking it again is allowed but changes nothing
    ("link an organisation", "POST", f"{PROJECT}organisation/", {"id": 1}, 2, 201, False),
    ("delete the project", "DELETE", PROJECT, None, 4, 204, True),
]


# Operations a read-only user is also allowed to do when their permission set has the matching additive permission
# (project_note for notes, document for documents) - only read_only_extra has them
ADDITIVE_ROLES = {"add a note": {"read_only_extra"}, "add a folder": {"read_only_extra"}}


def snapshot():
    return {model.__name__: list(model.objects.order_by("pk").values()) for model in TABLES}


class RoleDataEffectTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    @staticmethod
    def _client(role):
        client = APIClient()
        if role is not None:
            # force_login: a user in no group can not log in through the api but can still hold a session
            client.force_login(User.objects.get(username=role))
        return client

    def _run(self, role, method, url, body):
        """Run one request as a role, then roll the database back. Returns (response, data changed?)"""
        with transaction.atomic():
            before = snapshot()
            response = getattr(self._client(role), method.lower())(url, body, format="json")
            changed = snapshot() != before
            transaction.set_rollback(True)

        return response, changed

    def test_refused_requests_change_nothing_and_allowed_ones_do_what_they_should(self):
        for role, level in LEVEL_ON_QA_PROJECT.items():
            for name, method, url, body, needed, allowed_status, mutates in OPERATIONS:
                with self.subTest(role=role, operation=name):
                    response, changed = self._run(role, method, url, body)

                    if (level is not None and level >= needed) or role in ADDITIVE_ROLES.get(name, ()):
                        self.assertEqual(response.status_code, allowed_status, response.data)
                        self.assertEqual(changed, mutates)
                    else:
                        self.assertEqual(response.status_code, 403)
                        self.assertFalse(changed, "A refused request changed data")

    def test_anonymous_users_can_do_nothing(self):
        for name, method, url, body, *_ in OPERATIONS:
            with self.subTest(operation=name):
                response, changed = self._run(None, method, url, body)

                self.assertEqual(response.status_code, 403)
                self.assertFalse(changed)

    def test_the_project_the_role_can_not_reach_is_untouched_whatever_they_try(self):
        """Project 1 is Administration only: no QA role can read or change it"""
        for role in ("team_leader", "team_member", "team_intern", "read_only", "read_only_extra", "no_group"):
            for name, method, url, body, *_ in OPERATIONS:
                url_for_admin_project = url.replace("/project/2/", "/project/1/")
                with self.subTest(role=role, operation=name):
                    response, changed = self._run(role, method, url_for_admin_project, body)

                    self.assertEqual(response.status_code, 403)
                    self.assertFalse(changed)

    def test_dark_admin_is_a_superuser_but_only_reaches_their_own_group(self):
        """Group membership, not is_superuser, decides who can use the project api"""
        self.assertEqual(self._run("dark_admin", "GET", "/api/v1/project/1/", None)[0].status_code, 200)
        self.assertEqual(self._run("dark_admin", "GET", PROJECT, None)[0].status_code, 403)

    # ---------- creating a project: needs level 3 in some group, and only into groups you belong to ----------
    def test_who_can_create_a_project_and_in_which_groups(self):
        for role, level in LEVEL_ANYWHERE.items():
            for group in (1, 2, 3):
                with self.subTest(role=role, group=group):
                    response, changed = self._run(
                        role, "POST", "/api/v1/project/", {"title": "New", "group_list": [group]}
                    )

                    if level is None or level < 3:
                        self.assertEqual(response.status_code, 403)
                        self.assertFalse(changed)
                    elif group in CREATE_IN[role]:
                        self.assertEqual(response.status_code, 201, response.data)
                        self.assertTrue(changed)
                    else:
                        self.assertEqual(response.status_code, 400, "Created a project in someone else's group")
                        self.assertFalse(changed)

    # ---------- listing projects: only the ones in your groups ----------
    def test_the_project_list_only_has_projects_in_the_users_groups(self):
        visible = {"admin": {1, 2}, "dark_admin": {1}, **{role: {2} for role in LEVEL_ON_QA_PROJECT if role not in
                                                         ("admin", "dark_admin", "no_group")}}
        for role, expected in visible.items():
            with self.subTest(role=role):
                response = self._client(role).get("/api/v1/project/")

                self.assertEqual(response.status_code, 200)
                self.assertEqual({project["id"] for project in response.data["results"]}, expected)

    def test_a_user_with_no_group_gets_nothing_from_the_list(self):
        self.assertEqual(self._client("no_group").get("/api/v1/project/").status_code, 403)

    # ---------- the additive note and document permissions ----------
    @staticmethod
    def _set_permission_set(**fields):
        PermissionSet.objects.filter(name="Read Only + Extra").update(**fields)

    def test_the_extra_permissions_let_a_read_only_user_add_notes_and_documents(self):
        """Their permission set has project_note and document switched on - the additive permissions exist so a
        read-only user can still contribute notes and documents"""
        note, changed = self._run("read_only_extra", "POST", f"{PROJECT}notes/", {"note": "A note"})
        self.assertEqual(note.status_code, 201)
        self.assertTrue(changed)
        self.assertEqual(note.data["note"], "A note")

        folder, changed = self._run("read_only_extra", "POST", f"{PROJECT}documents/",
                                    {"type": "folder", "description": "F"})
        self.assertEqual(folder.status_code, 201)
        self.assertTrue(changed)

    def test_without_the_extra_permissions_a_read_only_user_still_can_not(self):
        for body_url, body in ((f"{PROJECT}notes/", {"note": "A note"}),
                               (f"{PROJECT}documents/", {"type": "folder", "description": "F"})):
            with self.subTest(url=body_url):
                response, changed = self._run("read_only", "POST", body_url, body)

                self.assertEqual(response.status_code, 403)
                self.assertFalse(changed)

    def test_each_extra_permission_only_unlocks_its_own_thing(self):
        self._set_permission_set(project_note=0)
        self.assertEqual(self._run("read_only_extra", "POST", f"{PROJECT}notes/", {"note": "x"})[0].status_code, 403)
        self.assertEqual(
            self._run("read_only_extra", "POST", f"{PROJECT}documents/", {"type": "folder", "description": "F"})[0]
            .status_code, 201)

        self._set_permission_set(project_note=1, document=0)
        self.assertEqual(self._run("read_only_extra", "POST", f"{PROJECT}notes/", {"note": "x"})[0].status_code, 201)
        self.assertEqual(
            self._run("read_only_extra", "POST", f"{PROJECT}documents/", {"type": "folder", "description": "F"})[0]
            .status_code, 403)

    def test_the_extra_permissions_do_not_unlock_anything_else(self):
        """Everything except notes and creating documents still needs the normal level"""
        for name, method, url, body, needed, _, _ in OPERATIONS:
            if name in ADDITIVE_ROLES:
                continue
            with self.subTest(operation=name):
                response, changed = self._run("read_only_extra", method, url, body)

                if needed > 1:
                    self.assertEqual(response.status_code, 403)
                    self.assertFalse(changed)

    def test_a_user_can_not_edit_or_delete_other_peoples_notes_with_the_extra_permission(self):
        """Notes belong to their author - the extra permission does not change that"""
        with transaction.atomic():
            leaders_note = self._client("team_leader").post(f"{PROJECT}notes/", {"note": "Leader's"}, format="json")
            note_url = f"{PROJECT}notes/{leaders_note.data['id']}/"
            before = snapshot()

            edit = self._client("read_only_extra").patch(note_url, {"note": "Hijacked"}, format="json")
            delete = self._client("read_only_extra").delete(note_url)

            self.assertEqual((edit.status_code, delete.status_code), (400, 400))  # not the author
            self.assertEqual(snapshot(), before)
            transaction.set_rollback(True)

    def test_a_user_can_edit_and_delete_their_own_notes_with_the_extra_permission(self):
        with transaction.atomic():
            client = self._client("read_only_extra")
            created = client.post(f"{PROJECT}notes/", {"note": "Mine"}, format="json")
            note_url = f"{PROJECT}notes/{created.data['id']}/"

            self.assertEqual(client.patch(note_url, {"note": "Mine, edited"}, format="json").status_code, 200)
            self.assertEqual(ObjectNote.objects.get(pk=created.data["id"]).note, "Mine, edited")
            self.assertEqual(client.delete(note_url).status_code, 204)
            self.assertTrue(ObjectNote.objects.get(pk=created.data["id"]).is_deleted)
            transaction.set_rollback(True)

    def test_the_extra_permission_does_not_let_someone_in_who_can_not_read_the_project(self):
        """It adds an ability to a read-only user - it is not a way in"""
        self._set_permission_set(project=0)

        for url, body in ((f"{PROJECT}notes/", {"note": "x"}), (f"{PROJECT}documents/", {"type": "folder", "description": "F"})):
            with self.subTest(url=url):
                response, changed = self._run("read_only_extra", "POST", url, body)

                self.assertEqual(response.status_code, 403)
                self.assertFalse(changed)

    def test_the_extra_permission_in_another_group_does_not_count(self):
        """Read access and the extra permission have to come from the same permission set: a user who reads through one
        group and has the extra permission only through another is still refused"""
        extra_only = PermissionSet.objects.create(
            name="Notes only", project=0, project_note=1, document=1,
            creation_user=User.objects.get(username="admin"), change_user=User.objects.get(username="admin"),
        )
        group = Group.objects.get(name="Empty Group")
        ObjectAssignment.objects.create(
            project_id=2, group=group,
            creation_user=User.objects.get(username="admin"), change_user=User.objects.get(username="admin"),
        )
        UserGroup.objects.create(
            username=User.objects.get(username="read_only"), group=group, permission_set=extra_only,
            creation_user=User.objects.get(username="admin"), change_user=User.objects.get(username="admin"),
        )

        response, changed = self._run("read_only", "POST", f"{PROJECT}notes/", {"note": "x"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(changed)
