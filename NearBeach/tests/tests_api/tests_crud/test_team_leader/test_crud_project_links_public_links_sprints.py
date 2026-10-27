"""CRUD tests for the link list, public links and sprints of a project, run as the team leader.

Fixture data for project 2 ("Project - QA Team"):
 - links (object assignments) 45 and 46 to requirements 1 and 2, 47 and 48 to tasks 1 and 2
 - link 42 belongs to project 1 but points back at project 2 (a reverse link)
 - one public link, 5f369dc9-a0bb-416d-9779-92576d0500bb (project 1 has 3d7346c4-05b6-41df-816a-eff814d9bbd0)
 - sprint 2 (project 1 has sprint 1)
"""
import uuid

from NearBeach.models.misc.misc import PublicLink
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.tests.tests_api.tests_crud.test_team_leader.test_crud_project import (
    QA_PROJECT_URL,
    TeamLeaderProjectBase,
)

LINK_URL = f"{QA_PROJECT_URL}link_list/"
PUBLIC_LINK_URL = f"{QA_PROJECT_URL}public_link/"
SPRINT_URL = f"{QA_PROJECT_URL}sprint/"

OWN_PUBLIC_LINK = "5f369dc9-a0bb-416d-9779-92576d0500bb"
OTHER_PUBLIC_LINK = "3d7346c4-05b6-41df-816a-eff814d9bbd0"
OTHER_PROJECT_LINK = 43  # project 1 -> task 1
OTHER_PROJECT_SPRINT = 1


class ProjectLinkListTests(TeamLeaderProjectBase):
    def _create(self, object_type="task", object_id=2, object_relation="relates"):
        return self.client.post(
            LINK_URL,
            {"object_type": object_type, "object_id": object_id, "object_relation": object_relation},
            format="json",
        )

    def _links(self):
        """(type, id) of every link row - kanban cards are left out, they are not links"""
        rows = self.client.get(LINK_URL).data
        return sorted((row["object_type"], row["object_id"]) for row in rows if row["object_type"] != "card")

    # ---------- list ----------
    def test_list_has_the_links_of_the_project(self):
        response = self.client.get(LINK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self._links(),
            [("project", 1), ("requirement", 1), ("requirement", 2), ("task", 1), ("task", 2)],
        )

    def test_list_is_not_paginated(self):
        self.assertIsInstance(self.client.get(LINK_URL).data, list)

    def test_link_rows_have_the_documented_fields(self):
        row = next(r for r in self.client.get(LINK_URL).data if r["object_type"] == "task" and r["object_id"] == 2)

        self.assertEqual(
            set(row),
            {
                "object_assignment_id", "object_id", "object_title", "object_status",
                "object_type", "parent_link", "link_relationship", "reverse_relation",
            },
        )
        self.assertEqual(row["object_assignment_id"], 48)
        self.assertEqual(row["object_title"], "Task - QA Team")
        self.assertEqual(row["link_relationship"], "Relate")
        self.assertEqual(row["parent_link"], "project")
        self.assertFalse(row["reverse_relation"])

    def test_a_link_pointing_back_at_the_project_is_a_reverse_link(self):
        row = next(r for r in self.client.get(LINK_URL).data if r["object_assignment_id"] == 42)

        self.assertTrue(row["reverse_relation"])
        self.assertEqual(row["object_type"], "project")

    def test_list_leaves_out_deleted_links(self):
        ObjectAssignment.objects.filter(pk=48).update(is_deleted=True)

        self.assertNotIn(("task", 2), self._links())

    def test_list_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/link_list/").status_code, 404)

    # ---------- create ----------
    def test_create_returns_the_new_link(self):
        response = self._create("task", 2, "relates")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["object_id"], 2)
        self.assertEqual(response.data["object_type"], "task")
        self.assertEqual(response.data["object_title"], "Task - QA Team")
        self.assertEqual(response.data["link_relationship"], "Relate")
        self.assertEqual(response.data["parent_link"], "project")
        self.assertFalse(response.data["reverse_relation"])

    def test_create_saves_the_link(self):
        response = self._create("task", 2, "relates")

        row = ObjectAssignment.objects.get(pk=response.data["object_assignment_id"])
        self.assertEqual((row.project_id, row.task_id), (2, 2))
        self.assertEqual(row.link_relationship, "Relate")
        self.assertEqual(row.parent_link, "project")
        self.assertEqual(row.change_user, self.leader)
        self.assertFalse(row.is_deleted)

    def test_the_relationship_decides_the_label_and_the_parent(self):
        cases = {
            "relates": ("Relate", "project"),
            "blocked_by": ("Block", "task"),
            "blocking": ("Block", "project"),
            "sub_object_of": ("Subobject", "task"),
            "parent_object_of": ("Subobject", "project"),
            "has_duplicate": ("Duplicate", "task"),
            "duplicate_object": ("Duplicate", "project"),
        }
        for relation, (label, parent) in cases.items():
            with self.subTest(relation):
                response = self._create("task", 2, relation)

                self.assertEqual(response.status_code, 201, response.data)
                self.assertEqual((response.data["link_relationship"], response.data["parent_link"]), (label, parent))

    def test_a_new_link_appears_in_the_list(self):
        created = self._create("requirement_item", 2).data["object_assignment_id"]

        ids = [row["object_assignment_id"] for row in self.client.get(LINK_URL).data]
        self.assertIn(created, ids)

    def test_linking_to_another_project(self):
        response = self._create("project", 1, "relates")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["object_type"], "project")
        row = ObjectAssignment.objects.get(pk=response.data["object_assignment_id"])
        self.assertEqual(row.meta_object, 1)

    def test_create_does_not_touch_other_projects(self):
        before = ObjectAssignment.objects.filter(project_id=1).count()

        self._create("task", 2)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=1).count(), before)

    def test_bad_links_are_rejected_and_nothing_is_saved(self):
        bodies = {
            "unknown type": {"object_type": "banana", "object_id": 1, "object_relation": "relates"},
            "unknown object": {"object_type": "task", "object_id": 99999, "object_relation": "relates"},
            "unknown relation": {"object_type": "task", "object_id": 1, "object_relation": "loves"},
            "missing relation": {"object_type": "task", "object_id": 1},
            "missing object": {"object_type": "task", "object_relation": "relates"},
            "missing type": {"object_id": 1, "object_relation": "relates"},
            "empty": {},
        }
        before = ObjectAssignment.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(LINK_URL, body, format="json").status_code, 400)

        self.assertEqual(ObjectAssignment.objects.count(), before)

    def test_cannot_link_to_objects_the_user_has_no_access_to(self):
        """Known bug - LinkListService.create never checks the user can see the object being linked, so the leader
        links to Administration-only objects and is sent their titles"""
        before = ObjectAssignment.objects.count()

        for object_type in ("project", "task", "requirement"):
            with self.subTest(object_type):
                response = self._create(object_type, 1, "relates")

                self.assertIn(response.status_code, (400, 403, 404), response.data)
                self.assertNotIn("Administration", str(response.data))

        self.assertEqual(ObjectAssignment.objects.count(), before)

    def test_create_missing_project_is_not_found(self):
        body = {"object_type": "task", "object_id": 1, "object_relation": "relates"}

        self.assertEqual(self.client.post("/api/v1/project/9999/link_list/", body, format="json").status_code, 404)

    # ---------- update ----------
    def _patch(self, link_id, object_type="task", object_id=1, object_relation="blocked_by"):
        return self.client.patch(
            f"{LINK_URL}{link_id}/",
            {"object_type": object_type, "object_id": object_id, "object_relation": object_relation},
            format="json",
        )

    def test_updating_a_link(self):
        response = self._patch(48, "task", 1, "blocked_by")

        self.assertEqual(response.status_code, 200, response.data)
        row = ObjectAssignment.objects.get(pk=48)
        self.assertEqual(row.task_id, 1)
        self.assertEqual(row.link_relationship, "Block")
        self.assertEqual(row.parent_link, "task")
        self.assertEqual(row.change_user, self.leader)

    def test_updating_moves_date_modified_forward(self):
        before = ObjectAssignment.objects.get(pk=48).date_modified

        self._patch(48)

        self.assertGreater(ObjectAssignment.objects.get(pk=48).date_modified, before)

    def test_updating_a_link_leaves_the_others_alone(self):
        before = ObjectAssignment.objects.get(pk=47).link_relationship

        self._patch(48)

        self.assertEqual(ObjectAssignment.objects.get(pk=47).link_relationship, before)

    def test_bad_updates_are_rejected_and_change_nothing(self):
        bodies = {
            "unknown object": {"object_type": "task", "object_id": 99999, "object_relation": "relates"},
            "unknown type": {"object_type": "banana", "object_id": 1, "object_relation": "relates"},
            "unknown relation": {"object_type": "task", "object_id": 1, "object_relation": "loves"},
            "empty": {},
        }
        before = ObjectAssignment.objects.values().get(pk=48)

        for name, body in bodies.items():
            with self.subTest(name):
                response = self.client.patch(f"{LINK_URL}48/", body, format="json")
                self.assertEqual(response.status_code, 400)

        self.assertEqual(ObjectAssignment.objects.values().get(pk=48), before)

    def test_links_that_are_not_on_this_project_cannot_be_updated(self):
        for link_id in (99999, OTHER_PROJECT_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self._patch(link_id).status_code, 400)

        self.assertEqual(ObjectAssignment.objects.get(pk=OTHER_PROJECT_LINK).project_id, 1)

    def test_a_deleted_link_cannot_be_updated(self):
        ObjectAssignment.objects.filter(pk=48).update(is_deleted=True)

        self.assertEqual(self._patch(48).status_code, 400)

    # ---------- delete ----------
    def test_deleting_a_link(self):
        response = self.client.delete(f"{LINK_URL}48/")

        self.assertEqual(response.status_code, 204)
        self.assertNotIn(("task", 2), self._links())

    def test_delete_is_a_soft_delete(self):
        self.client.delete(f"{LINK_URL}48/")

        row = ObjectAssignment.objects.get(pk=48)
        self.assertTrue(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_deleting_a_link_leaves_the_others_alone(self):
        self.client.delete(f"{LINK_URL}48/")

        self.assertEqual(
            self._links(),
            [("project", 1), ("requirement", 1), ("requirement", 2), ("task", 1)],
        )

    def test_deleting_twice_is_rejected(self):
        self.client.delete(f"{LINK_URL}48/")

        self.assertEqual(self.client.delete(f"{LINK_URL}48/").status_code, 400)

    def test_links_that_are_not_on_this_project_cannot_be_deleted(self):
        for link_id in (99999, OTHER_PROJECT_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self.client.delete(f"{LINK_URL}{link_id}/").status_code, 400)

        self.assertFalse(ObjectAssignment.objects.get(pk=OTHER_PROJECT_LINK).is_deleted)

    def test_delete_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete("/api/v1/project/9999/link_list/48/").status_code, 404)


class ProjectPublicLinkTests(TeamLeaderProjectBase):
    def _ids(self):
        return [link["id"] for link in self.client.get(PUBLIC_LINK_URL).data]

    # ---------- list ----------
    def test_list_has_the_public_links_of_the_project(self):
        response = self.client.get(PUBLIC_LINK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": OWN_PUBLIC_LINK, "is_active": True}])

    def test_list_leaves_out_deleted_links_and_other_projects(self):
        PublicLink.objects.filter(pk=OWN_PUBLIC_LINK).update(is_deleted=True)

        self.assertEqual(self._ids(), [])

    def test_list_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/public_link/").status_code, 404)

    # ---------- create ----------
    def test_create_returns_the_new_link(self):
        response = self.client.post(PUBLIC_LINK_URL, {}, format="json")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(set(response.data), {"id", "is_active"})
        uuid.UUID(str(response.data["id"]))

    def test_create_saves_the_link_against_the_project(self):
        response = self.client.post(PUBLIC_LINK_URL, {}, format="json")

        link = PublicLink.objects.get(pk=response.data["id"])
        self.assertEqual(link.project_id, 2)
        self.assertEqual(link.creation_user, self.leader)
        self.assertEqual(link.change_user, self.leader)
        self.assertFalse(link.is_deleted)

    def test_a_new_link_appears_in_the_list(self):
        created = self.client.post(PUBLIC_LINK_URL, {}, format="json").data["id"]

        self.assertEqual(sorted(self._ids()), sorted([OWN_PUBLIC_LINK, str(created)]))

    def test_every_create_makes_a_different_link(self):
        first = self.client.post(PUBLIC_LINK_URL, {}, format="json").data["id"]
        second = self.client.post(PUBLIC_LINK_URL, {}, format="json").data["id"]

        self.assertNotEqual(first, second)

    def test_create_does_not_touch_other_projects(self):
        before = PublicLink.objects.filter(project_id=1).count()

        self.client.post(PUBLIC_LINK_URL, {}, format="json")

        self.assertEqual(PublicLink.objects.filter(project_id=1).count(), before)

    def test_create_missing_project_is_not_found(self):
        self.assertEqual(self.client.post("/api/v1/project/9999/public_link/", {}, format="json").status_code, 404)

    # ---------- update ----------
    def _patch(self, link_id, body):
        return self.client.patch(f"{PUBLIC_LINK_URL}{link_id}/", body, format="json")

    def test_switching_a_link_off_and_on(self):
        off = self._patch(OWN_PUBLIC_LINK, {"is_active": False})
        self.assertEqual(off.status_code, 200, off.data)
        self.assertFalse(off.data["is_active"])
        self.assertFalse(PublicLink.objects.get(pk=OWN_PUBLIC_LINK).is_active)

        on = self._patch(OWN_PUBLIC_LINK, {"is_active": True})
        self.assertTrue(on.data["is_active"])
        self.assertTrue(PublicLink.objects.get(pk=OWN_PUBLIC_LINK).is_active)

    def test_update_records_who_made_the_change(self):
        self._patch(OWN_PUBLIC_LINK, {"is_active": False})

        link = PublicLink.objects.get(pk=OWN_PUBLIC_LINK)
        self.assertEqual(link.change_user, self.leader)

    def test_update_does_not_touch_other_projects(self):
        self._patch(OWN_PUBLIC_LINK, {"is_active": False})

        self.assertTrue(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_active)

    def test_update_needs_is_active(self):
        for name, body in {"empty": {}, "null": {"is_active": None}}.items():
            with self.subTest(name):
                self.assertEqual(self._patch(OWN_PUBLIC_LINK, body).status_code, 400)

        self.assertTrue(PublicLink.objects.get(pk=OWN_PUBLIC_LINK).is_active)

    def test_links_that_are_not_on_this_project_cannot_be_updated(self):
        for link_id in (str(uuid.uuid4()), OTHER_PUBLIC_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self._patch(link_id, {"is_active": False}).status_code, 400)

        self.assertTrue(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_active)

    def test_a_deleted_link_cannot_be_updated(self):
        PublicLink.objects.filter(pk=OWN_PUBLIC_LINK).update(is_deleted=True)

        self.assertEqual(self._patch(OWN_PUBLIC_LINK, {"is_active": False}).status_code, 400)

    # ---------- delete ----------
    def test_deleting_a_link(self):
        response = self.client.delete(f"{PUBLIC_LINK_URL}{OWN_PUBLIC_LINK}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self._ids(), [])

    def test_delete_is_a_soft_delete(self):
        self.client.delete(f"{PUBLIC_LINK_URL}{OWN_PUBLIC_LINK}/")

        link = PublicLink.objects.get(pk=OWN_PUBLIC_LINK)
        self.assertTrue(link.is_deleted)
        self.assertEqual(link.change_user, self.leader)

    def test_deleting_twice_is_rejected(self):
        self.client.delete(f"{PUBLIC_LINK_URL}{OWN_PUBLIC_LINK}/")

        self.assertEqual(self.client.delete(f"{PUBLIC_LINK_URL}{OWN_PUBLIC_LINK}/").status_code, 400)

    def test_links_that_are_not_on_this_project_cannot_be_deleted(self):
        for link_id in (str(uuid.uuid4()), OTHER_PUBLIC_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self.client.delete(f"{PUBLIC_LINK_URL}{link_id}/").status_code, 400)

        self.assertFalse(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_deleted)

    def test_delete_missing_project_is_not_found(self):
        response = self.client.delete(f"/api/v1/project/9999/public_link/{OWN_PUBLIC_LINK}/")

        self.assertEqual(response.status_code, 404)


class ProjectSprintTests(TeamLeaderProjectBase):
    START = "2026-05-04T09:00:00Z"
    END = "2026-05-18T17:00:00Z"

    def _create(self, **overrides):
        body = {"title": "Leader sprint", "start_date": self.START, "end_date": self.END, **overrides}
        return self.client.post(SPRINT_URL, body, format="json")

    def _ids(self):
        return [sprint["id"] for sprint in self.client.get(SPRINT_URL).data]

    # ---------- list ----------
    def test_list_has_the_sprints_of_the_project(self):
        response = self.client.get(SPRINT_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._ids(), [2])

    def test_sprint_rows_have_the_documented_fields(self):
        sprint = self.client.get(SPRINT_URL).data[0]

        self.assertEqual(sprint["title"], "project-2 - Sprint 1 - 18 Mar 2024")
        self.assertEqual(sprint["status"], "Draft")
        for field in ("total_story_points", "completed_story_points", "start_date", "end_date", "project"):
            self.assertIn(field, sprint)

    def test_list_is_sorted_by_start_date(self):
        later = self._create(title="Later", start_date="2027-01-01T00:00:00Z", end_date="2027-01-08T00:00:00Z")
        earlier = self._create(title="Earlier", start_date="2020-01-01T00:00:00Z", end_date="2020-01-08T00:00:00Z")

        self.assertEqual(self._ids(), [earlier.data["id"], 2, later.data["id"]])

    def test_list_leaves_out_deleted_sprints_and_other_projects(self):
        Sprint.objects.filter(pk=2).update(is_deleted=True)

        self.assertEqual(self._ids(), [])

    def test_list_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/sprint/").status_code, 404)

    # ---------- create ----------
    def test_create_returns_the_new_sprint(self):
        response = self._create()

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["title"], "Leader sprint")
        self.assertEqual(response.data["start_date"], self.START)
        self.assertEqual(response.data["end_date"], self.END)

    def test_create_saves_the_sprint_against_the_project(self):
        response = self._create()

        sprint = Sprint.objects.get(pk=response.data["id"])
        self.assertEqual(sprint.project_id, 2)
        self.assertIsNone(sprint.requirement_id)
        self.assertEqual(sprint.title, "Leader sprint")
        self.assertEqual(sprint.creation_user, self.leader)
        self.assertEqual(sprint.change_user, self.leader)
        self.assertFalse(sprint.is_deleted)

    def test_a_new_sprint_starts_as_a_draft_with_no_story_points(self):
        sprint = Sprint.objects.get(pk=self._create().data["id"])

        self.assertEqual(sprint.status, "Draft")
        self.assertEqual((sprint.total_story_points, sprint.completed_story_points), (0, 0))

    def test_a_new_sprint_appears_in_the_list(self):
        created = self._create().data["id"]

        self.assertEqual(self._ids(), [2, created])

    def test_create_does_not_touch_other_projects(self):
        before = Sprint.objects.filter(project_id=1).count()

        self._create()

        self.assertEqual(Sprint.objects.filter(project_id=1).count(), before)

    def test_bad_sprints_are_rejected_and_nothing_is_saved(self):
        bodies = {
            "no title": {"start_date": self.START, "end_date": self.END},
            "blank title": {"title": "", "start_date": self.START, "end_date": self.END},
            "no start": {"title": "x", "end_date": self.END},
            "no end": {"title": "x", "start_date": self.START},
            "bad date": {"title": "x", "start_date": "tomorrow", "end_date": self.END},
        }
        before = Sprint.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(SPRINT_URL, body, format="json").status_code, 400)

        self.assertEqual(Sprint.objects.count(), before)

    def test_create_missing_project_is_not_found(self):
        body = {"title": "x", "start_date": self.START, "end_date": self.END}

        self.assertEqual(self.client.post("/api/v1/project/9999/sprint/", body, format="json").status_code, 404)

    # ---------- delete ----------
    def test_deleting_a_sprint(self):
        response = self.client.delete(f"{SPRINT_URL}2/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self._ids(), [])

    def test_delete_is_a_soft_delete(self):
        self.client.delete(f"{SPRINT_URL}2/")

        sprint = Sprint.objects.get(pk=2)
        self.assertTrue(sprint.is_deleted)
        self.assertEqual(sprint.change_user, self.leader)

    def test_deleting_a_sprint_leaves_the_others_alone(self):
        created = self._create().data["id"]

        self.client.delete(f"{SPRINT_URL}2/")

        self.assertEqual(self._ids(), [created])

    def test_deleting_twice_is_rejected(self):
        self.client.delete(f"{SPRINT_URL}2/")

        self.assertEqual(self.client.delete(f"{SPRINT_URL}2/").status_code, 400)

    def test_sprints_that_are_not_on_this_project_cannot_be_deleted(self):
        for sprint_id in (99999, OTHER_PROJECT_SPRINT):
            with self.subTest(sprint_id=sprint_id):
                self.assertEqual(self.client.delete(f"{SPRINT_URL}{sprint_id}/").status_code, 400)

        self.assertFalse(Sprint.objects.get(pk=OTHER_PROJECT_SPRINT).is_deleted)

    def test_delete_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete("/api/v1/project/9999/sprint/2/").status_code, 404)
