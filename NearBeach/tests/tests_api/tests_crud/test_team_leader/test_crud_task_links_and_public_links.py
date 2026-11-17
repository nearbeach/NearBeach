"""CRUD tests for the link list and public links of a task, run as the team leader.

Fixture data for task 2 ("Task - QA Team"):
 - links (object assignments) 44 and 48 to projects 1 and 2, 55 and 56 to requirements 1 and 2
 - link 57 belongs to task 1 but points back at task 2 (a reverse link)
 - one public link, c5994697-a7e6-4e54-b8b1-4dee7315d7ea (task 1 has 1c1067e9-563f-4419-9dac-e87d757ecb37)
"""
import uuid

from NearBeach.models.misc.misc import PublicLink
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.tests.tests_api.tests_crud.test_team_leader.test_crud_task import (
    QA_PROJECT_URL,
    TeamLeaderTaskBase,
)

LINK_URL = f"{QA_PROJECT_URL}link_list/"
PUBLIC_LINK_URL = f"{QA_PROJECT_URL}public_link/"

OWN_PUBLIC_LINK = "c5994697-a7e6-4e54-b8b1-4dee7315d7ea"
OTHER_PUBLIC_LINK = "1c1067e9-563f-4419-9dac-e87d757ecb37"
OTHER_PROJECT_LINK = 43  # task 1 -> project 1


class TaskLinkListTests(TeamLeaderTaskBase):
    def _create(self, object_type="project", object_id=2, object_relation="relates"):
        return self.client.post(
            LINK_URL,
            {"object_type": object_type, "object_id": object_id, "object_relation": object_relation},
            format="json",
        )

    @staticmethod
    def _free_the_fixture_link():
        """The fixture already links the QA task to project 2 (row 48) and the same pair can not be linked twice"""
        ObjectAssignment.objects.filter(pk=48).update(is_deleted=True)

    def _links(self):
        """(type, id) of every link row - kanban cards are left out, they are not links"""
        rows = self.client.get(LINK_URL).data
        return sorted((row["object_type"], row["object_id"]) for row in rows if row["object_type"] != "card")

    # ---------- list ----------
    def test_list_has_the_links_of_the_task(self):
        response = self.client.get(LINK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self._links(),
            [("project", 1), ("project", 2), ("requirement", 1), ("requirement", 2), ("task", 1)],
        )

    def test_list_is_not_paginated(self):
        self.assertIsInstance(self.client.get(LINK_URL).data, list)

    def test_link_rows_have_the_documented_fields(self):
        row = next(r for r in self.client.get(LINK_URL).data if r["object_type"] == "project" and r["object_id"] == 2)

        self.assertEqual(
            set(row),
            {
                "object_assignment_id", "object_id", "object_title", "object_status",
                "object_type", "parent_link", "link_relationship", "reverse_relation",
            },
        )
        self.assertEqual(row["object_assignment_id"], 48)
        self.assertEqual(row["object_title"], "Project - QA Team")
        self.assertEqual(row["link_relationship"], "Relate")
        self.assertEqual(row["parent_link"], "project")  # fixture row 48: the project is the parent
        self.assertFalse(row["reverse_relation"])

    def test_a_link_pointing_back_at_the_task_is_a_reverse_link(self):
        row = next(r for r in self.client.get(LINK_URL).data if r["object_assignment_id"] == 57)

        self.assertTrue(row["reverse_relation"])
        self.assertEqual(row["object_type"], "task")

    def test_list_leaves_out_deleted_links(self):
        ObjectAssignment.objects.filter(pk=48).update(is_deleted=True)

        self.assertNotIn(("project", 2), self._links())

    def test_list_missing_task_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/task/9999/link_list/").status_code, 404)

    # ---------- create ----------
    def test_create_returns_the_new_link(self):
        self._free_the_fixture_link()
        response = self._create("project", 2, "relates")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["object_id"], 2)
        self.assertEqual(response.data["object_type"], "project")
        self.assertEqual(response.data["object_title"], "Project - QA Team")
        self.assertEqual(response.data["link_relationship"], "Relate")
        self.assertEqual(response.data["parent_link"], "task")
        self.assertFalse(response.data["reverse_relation"])

    def test_create_saves_the_link(self):
        self._free_the_fixture_link()
        response = self._create("project", 2, "relates")

        row = ObjectAssignment.objects.get(pk=response.data["object_assignment_id"])
        self.assertEqual((row.task_id, row.project_id), (2, 2))
        self.assertEqual(row.link_relationship, "Relate")
        self.assertEqual(row.parent_link, "task")
        self.assertEqual(row.change_user, self.leader)
        self.assertFalse(row.is_deleted)

    def test_the_relationship_decides_the_label_and_the_parent(self):
        cases = {
            "relates": ("Relate", "task"),
            "blocked_by": ("Block", "project"),
            "blocking": ("Block", "task"),
            "sub_object_of": ("Subobject", "project"),
            "parent_object_of": ("Subobject", "task"),
            "has_duplicate": ("Duplicate", "project"),
            "duplicate_object": ("Duplicate", "task"),
        }
        for relation, (label, parent) in cases.items():
            with self.subTest(relation):
                self._free_the_fixture_link()
                response = self._create("project", 2, relation)

                self.assertEqual(response.status_code, 201, response.data)
                self.assertEqual((response.data["link_relationship"], response.data["parent_link"]), (label, parent))
                ObjectAssignment.objects.filter(pk=response.data["object_assignment_id"]).update(is_deleted=True)

    def test_a_new_link_appears_in_the_list(self):
        created = self._create("requirement_item", 2).data["object_assignment_id"]
    
        ids = [row["object_assignment_id"] for row in self.client.get(LINK_URL).data]
        self.assertIn(created, ids)

    def test_linking_to_another_task(self):
        """Only a link between two objects of the same type sets meta_object (the other task)"""
        other_task = self.client.post(
            "/api/v1/task/", {"title": "Other QA task", "group_list": [2]}, format="json"
        ).data["id"]

        response = self._create("task", other_task, "relates")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["object_type"], "task")
        row = ObjectAssignment.objects.get(pk=response.data["object_assignment_id"])
        self.assertEqual(row.meta_object, other_task)
        self.assertEqual(row.meta_object_title, "Other QA task")

    def test_linking_to_a_child_object_needs_access_to_its_parent(self):
        """Requirement items have no group of their own - the leader reaches item 2 through requirement 2"""
        allowed = self._create("requirement_item", 2)
        self.assertEqual(allowed.status_code, 201, allowed.data)

        # Item 1 belongs to a requirement in the Administration group only
        denied = self._create("requirement_item", 1)
        self.assertEqual(denied.status_code, 403)

    def test_the_same_object_can_not_be_linked_twice(self):
        response = self._create("project", 2, "relates")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "Object already exists")

    def test_create_does_not_touch_other_tasks(self):
        before = ObjectAssignment.objects.filter(task_id=1).count()

        self._create("project", 2)

        self.assertEqual(ObjectAssignment.objects.filter(task_id=1).count(), before)

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
                # A referenced object that does not exist is a 404 - anything malformed is a 400
                expected = 404 if name == "unknown object" else 400
                self.assertEqual(self.client.post(LINK_URL, body, format="json").status_code, expected)

        self.assertEqual(ObjectAssignment.objects.count(), before)

    def test_cannot_link_to_objects_the_user_has_no_access_to(self):
        """Regression - LinkListService.create once never checked the user could see the object being linked, so the
        leader could link to Administration-only objects and was sent their titles"""
        before = ObjectAssignment.objects.count()

        for object_type in ("task", "task", "requirement"):
            with self.subTest(object_type):
                response = self._create(object_type, 1, "relates")

                self.assertIn(response.status_code, (400, 403, 404), response.data)
                self.assertNotIn("Administration", str(response.data))

        self.assertEqual(ObjectAssignment.objects.count(), before)

    def test_create_missing_task_is_not_found(self):
        body = {"object_type": "task", "object_id": 1, "object_relation": "relates"}

        self.assertEqual(self.client.post("/api/v1/task/9999/link_list/", body, format="json").status_code, 404)

    # ---------- update ----------
    def _patch(self, link_id, object_type="project", object_id=1, object_relation="blocked_by"):
        return self.client.patch(
            f"{LINK_URL}{link_id}/",
            {"object_type": object_type, "object_id": object_id, "object_relation": object_relation},
            format="json",
        )

    def test_updating_a_link(self):
        response = self._patch(48, "project", 1, "blocked_by")

        self.assertEqual(response.status_code, 200, response.data)
        row = ObjectAssignment.objects.get(pk=48)
        self.assertEqual((row.task_id, row.project_id), (2, 1))
        self.assertEqual(row.link_relationship, "Block")
        self.assertEqual(row.parent_link, "project")
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
                # A referenced object that does not exist is a 404 - anything malformed is a 400
                self.assertEqual(response.status_code, 404 if name == "unknown object" else 400)

        self.assertEqual(ObjectAssignment.objects.values().get(pk=48), before)

    def test_links_that_are_not_on_this_task_cannot_be_updated(self):
        for link_id in (99999, OTHER_PROJECT_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self._patch(link_id).status_code, 404)

        self.assertEqual(ObjectAssignment.objects.get(pk=OTHER_PROJECT_LINK).task_id, 1)

    def test_a_deleted_link_cannot_be_updated(self):
        ObjectAssignment.objects.filter(pk=48).update(is_deleted=True)

        self.assertEqual(self._patch(48).status_code, 404)

    # ---------- delete ----------
    def test_deleting_a_link(self):
        response = self.client.delete(f"{LINK_URL}48/")

        self.assertEqual(response.status_code, 204)
        self.assertNotIn(("project", 2), self._links())

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

        self.assertEqual(self.client.delete(f"{LINK_URL}48/").status_code, 404)

    def test_links_that_are_not_on_this_task_cannot_be_deleted(self):
        for link_id in (99999, OTHER_PROJECT_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self.client.delete(f"{LINK_URL}{link_id}/").status_code, 404)

        self.assertFalse(ObjectAssignment.objects.get(pk=OTHER_PROJECT_LINK).is_deleted)

    def test_delete_missing_task_is_not_found(self):
        self.assertEqual(self.client.delete("/api/v1/task/9999/link_list/48/").status_code, 404)


class TaskPublicLinkTests(TeamLeaderTaskBase):
    def _ids(self):
        return [link["id"] for link in self.client.get(PUBLIC_LINK_URL).data]

    # ---------- list ----------
    def test_list_has_the_public_links_of_the_task(self):
        response = self.client.get(PUBLIC_LINK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": OWN_PUBLIC_LINK, "is_active": True}])

    def test_list_leaves_out_deleted_links_and_other_tasks(self):
        PublicLink.objects.filter(pk=OWN_PUBLIC_LINK).update(is_deleted=True)

        self.assertEqual(self._ids(), [])

    def test_list_missing_task_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/task/9999/public_link/").status_code, 404)

    # ---------- create ----------
    def test_create_returns_the_new_link(self):
        response = self.client.post(PUBLIC_LINK_URL, {}, format="json")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(set(response.data), {"id", "is_active"})
        uuid.UUID(str(response.data["id"]))

    def test_create_saves_the_link_against_the_task(self):
        response = self.client.post(PUBLIC_LINK_URL, {}, format="json")

        link = PublicLink.objects.get(pk=response.data["id"])
        self.assertEqual(link.task_id, 2)
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

    def test_create_does_not_touch_other_tasks(self):
        before = PublicLink.objects.filter(task_id=1).count()

        self.client.post(PUBLIC_LINK_URL, {}, format="json")

        self.assertEqual(PublicLink.objects.filter(task_id=1).count(), before)

    def test_create_missing_task_is_not_found(self):
        self.assertEqual(self.client.post("/api/v1/task/9999/public_link/", {}, format="json").status_code, 404)

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

    def test_update_does_not_touch_other_tasks(self):
        self._patch(OWN_PUBLIC_LINK, {"is_active": False})

        self.assertTrue(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_active)

    def test_update_needs_is_active(self):
        for name, body in {"empty": {}, "null": {"is_active": None}}.items():
            with self.subTest(name):
                self.assertEqual(self._patch(OWN_PUBLIC_LINK, body).status_code, 400)

        self.assertTrue(PublicLink.objects.get(pk=OWN_PUBLIC_LINK).is_active)

    def test_links_that_are_not_on_this_task_cannot_be_updated(self):
        for link_id in (str(uuid.uuid4()), OTHER_PUBLIC_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self._patch(link_id, {"is_active": False}).status_code, 404)

        self.assertTrue(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_active)

    def test_a_deleted_link_cannot_be_updated(self):
        PublicLink.objects.filter(pk=OWN_PUBLIC_LINK).update(is_deleted=True)

        self.assertEqual(self._patch(OWN_PUBLIC_LINK, {"is_active": False}).status_code, 404)

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

        self.assertEqual(self.client.delete(f"{PUBLIC_LINK_URL}{OWN_PUBLIC_LINK}/").status_code, 404)

    def test_links_that_are_not_on_this_task_cannot_be_deleted(self):
        for link_id in (str(uuid.uuid4()), OTHER_PUBLIC_LINK):
            with self.subTest(link_id=link_id):
                self.assertEqual(self.client.delete(f"{PUBLIC_LINK_URL}{link_id}/").status_code, 404)

        self.assertFalse(PublicLink.objects.get(pk=OTHER_PUBLIC_LINK).is_deleted)

    def test_delete_missing_task_is_not_found(self):
        response = self.client.delete(f"/api/v1/task/9999/public_link/{OWN_PUBLIC_LINK}/")

        self.assertEqual(response.status_code, 404)
