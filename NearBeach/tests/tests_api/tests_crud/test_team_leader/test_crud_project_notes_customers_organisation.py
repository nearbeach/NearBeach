"""CRUD tests for the notes, customers and organisation of a project, run as the team leader.

Fixture data for project 2 ("Project - QA Team"):
 - notes 3, 7 and 9, all written by the team leader
 - customer 1 linked, customer 2 not
 - organisation 1 ("NearBeach Incorporate") whose customers are 1 and 2
"""
from django.contrib.auth import get_user_model

from NearBeach.models.customer import Customer
from NearBeach.models.misc.note import ObjectNote
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.organisation import Organisation
from NearBeach.models.project import Project
from NearBeach.tests.tests_api.tests_crud.test_team_leader.test_crud_project import (
    QA_PROJECT_URL,
    TeamLeaderProjectBase,
)

NOTES_URL = f"{QA_PROJECT_URL}notes/"
CUSTOMER_URL = f"{QA_PROJECT_URL}customer/"
ORGANISATION_URL = f"{QA_PROJECT_URL}organisation/"

LEADER_NOTES = [3, 7, 9]
OTHER_PROJECT_NOTE = 2  # project 1, written by admin


class ProjectNoteBase(TeamLeaderProjectBase):
    def _admin_note(self, text="<p>Written by the admin</p>"):
        return ObjectNote.objects.create(project_id=2, note=text, creation_user=self.admin, change_user=self.admin)


class ProjectNoteListTests(ProjectNoteBase):
    def test_list_has_the_notes_of_the_project(self):
        response = self.client.get(NOTES_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(note["id"] for note in response.data), LEADER_NOTES)

    def test_note_rows_have_the_documented_fields(self):
        note = self.client.get(NOTES_URL).data[0]

        self.assertEqual(
            set(note),
            {"id", "note", "first_name", "last_name", "username", "profile_picture", "date_modified", "can_edit"},
        )
        self.assertEqual((note["first_name"], note["last_name"]), ("Team", "Leader"))
        self.assertEqual(note["username"], self.leader.pk)

    def test_can_edit_is_only_true_for_the_users_own_notes(self):
        admin_note = self._admin_note()

        notes = {note["id"]: note for note in self.client.get(NOTES_URL).data}

        self.assertTrue(notes[3]["can_edit"])
        self.assertFalse(notes[admin_note.pk]["can_edit"])

    def test_list_leaves_out_other_projects_and_deleted_notes(self):
        ObjectNote.objects.filter(pk=7).update(is_deleted=True)

        ids = [note["id"] for note in self.client.get(NOTES_URL).data]

        self.assertEqual(sorted(ids), [3, 9])
        self.assertNotIn(OTHER_PROJECT_NOTE, ids)

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/notes/").status_code, 404)


class ProjectNoteCreateTests(ProjectNoteBase):
    def _create(self, note="<p>A new note</p>"):
        return self.client.post(NOTES_URL, {"note": note}, format="json")

    def test_create_returns_the_note(self):
        response = self._create()

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["note"], "<p>A new note</p>")
        self.assertEqual(response.data["username"], self.leader.pk)
        self.assertTrue(response.data["can_edit"])
        self.assertEqual((response.data["first_name"], response.data["last_name"]), ("Team", "Leader"))

    def test_create_saves_the_note_against_the_project(self):
        response = self._create()

        note = ObjectNote.objects.get(pk=response.data["id"])
        self.assertEqual(note.project_id, 2)
        self.assertEqual(note.note, "<p>A new note</p>")
        self.assertEqual(note.creation_user, self.leader)
        self.assertEqual(note.change_user, self.leader)
        self.assertFalse(note.is_deleted)

    def test_a_new_note_appears_in_the_list(self):
        created = self._create().data["id"]

        self.assertIn(created, [note["id"] for note in self.client.get(NOTES_URL).data])

    def test_create_does_not_touch_other_projects(self):
        before = ObjectNote.objects.filter(project_id=1).count()

        self._create()

        self.assertEqual(ObjectNote.objects.filter(project_id=1).count(), before)

    def test_bad_notes_are_rejected_and_nothing_is_saved(self):
        bodies = {"missing": {}, "blank": {"note": ""}, "null": {"note": None}}
        before = ObjectNote.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                response = self.client.post(NOTES_URL, body, format="json")
                self.assertEqual(response.status_code, 400, response.data)
                self.assertIn("note", response.data)

        self.assertEqual(ObjectNote.objects.count(), before)

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.post("/api/v1/project/9999/notes/", {"note": "x"}, format="json").status_code, 404)


class ProjectNoteUpdateTests(ProjectNoteBase):
    def _patch(self, note_id, body):
        return self.client.patch(f"{NOTES_URL}{note_id}/", body, format="json")

    def test_updating_own_note(self):
        response = self._patch(3, {"note": "<p>Edited</p>"})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["id"], 3)
        self.assertEqual(response.data["note"], "<p>Edited</p>")
        self.assertEqual(ObjectNote.objects.get(pk=3).note, "<p>Edited</p>")

    def test_update_moves_date_modified_forward(self):
        before = ObjectNote.objects.get(pk=3).date_modified

        self._patch(3, {"note": "<p>Edited</p>"})

        self.assertGreater(ObjectNote.objects.get(pk=3).date_modified, before)

    def test_update_only_changes_that_note(self):
        before = {note.pk: note.note for note in ObjectNote.objects.exclude(pk=3)}

        self._patch(3, {"note": "<p>Edited</p>"})

        self.assertEqual({note.pk: note.note for note in ObjectNote.objects.exclude(pk=3)}, before)

    def test_a_note_written_by_someone_else_cannot_be_edited(self):
        note = self._admin_note()

        response = self._patch(note.pk, {"note": "<p>Hijacked</p>"})

        self.assertEqual(response.status_code, 400)
        note.refresh_from_db()
        self.assertEqual(note.note, "<p>Written by the admin</p>")
        self.assertEqual(note.change_user, self.admin)

    def test_bad_notes_are_rejected_and_change_nothing(self):
        original = ObjectNote.objects.get(pk=3).note

        for name, body in {"missing": {}, "blank": {"note": ""}}.items():
            with self.subTest(name):
                response = self._patch(3, body)
                self.assertEqual(response.status_code, 400, response.data)
                self.assertIn("note", response.data)

        self.assertEqual(ObjectNote.objects.get(pk=3).note, original)

    def test_notes_that_do_not_exist_on_this_project_are_not_found(self):
        cases = {"missing": 9999, "other project": OTHER_PROJECT_NOTE}
        for name, note_id in cases.items():
            with self.subTest(name):
                self.assertEqual(self._patch(note_id, {"note": "x"}).status_code, 404)

        self.assertNotEqual(ObjectNote.objects.get(pk=OTHER_PROJECT_NOTE).note, "x")

    def test_a_deleted_note_is_not_found(self):
        ObjectNote.objects.filter(pk=3).update(is_deleted=True)

        self.assertEqual(self._patch(3, {"note": "x"}).status_code, 404)


class ProjectNoteDeleteTests(ProjectNoteBase):
    def test_deleting_own_note(self):
        response = self.client.delete(f"{NOTES_URL}3/")

        self.assertEqual(response.status_code, 204)

    def test_delete_is_a_soft_delete(self):
        self.client.delete(f"{NOTES_URL}3/")

        note = ObjectNote.objects.get(pk=3)
        self.assertTrue(note.is_deleted)
        self.assertEqual(note.change_user, self.leader)

    def test_a_deleted_note_leaves_the_list_and_the_others_stay(self):
        self.client.delete(f"{NOTES_URL}3/")

        self.assertEqual(sorted(note["id"] for note in self.client.get(NOTES_URL).data), [7, 9])

    def test_deleting_twice_is_not_found(self):
        self.client.delete(f"{NOTES_URL}3/")

        self.assertEqual(self.client.delete(f"{NOTES_URL}3/").status_code, 404)

    def test_a_note_written_by_someone_else_cannot_be_deleted(self):
        note = self._admin_note()

        response = self.client.delete(f"{NOTES_URL}{note.pk}/")

        self.assertEqual(response.status_code, 400)
        note.refresh_from_db()
        self.assertFalse(note.is_deleted)

    def test_notes_that_do_not_exist_on_this_project_are_not_found(self):
        for note_id in (9999, OTHER_PROJECT_NOTE):
            with self.subTest(note_id=note_id):
                self.assertEqual(self.client.delete(f"{NOTES_URL}{note_id}/").status_code, 404)

        self.assertFalse(ObjectNote.objects.get(pk=OTHER_PROJECT_NOTE).is_deleted)


class ProjectCustomerTests(TeamLeaderProjectBase):
    def _add(self, customer_id):
        return self.client.post(CUSTOMER_URL, {"id": customer_id}, format="json")

    @staticmethod
    def _rows(customer_id, project_id=2):
        return ObjectAssignment.objects.filter(project_id=project_id, customer_id=customer_id)

    def _ids(self):
        return sorted(customer["id"] for customer in self.client.get(CUSTOMER_URL).data)

    # ---------- list ----------
    def test_list_has_the_linked_customers(self):
        response = self.client.get(CUSTOMER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._ids(), [1])
        self.assertTrue({"id", "first_name", "last_name", "email"} <= set(response.data[0]))

    def test_list_is_not_paginated(self):
        self.assertIsInstance(self.client.get(CUSTOMER_URL).data, list)

    def test_list_leaves_out_unlinked_customers(self):
        self.assertNotIn(2, self._ids())

    def test_list_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/customer/").status_code, 404)

    # ---------- link ----------
    def test_linking_returns_the_customer_list(self):
        response = self._add(2)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(sorted(customer["id"] for customer in response.data), [1, 2])

    def test_linking_saves_the_assignment(self):
        self._add(2)

        row = self._rows(2).get()
        self.assertFalse(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_linking_does_not_touch_other_projects(self):
        before = ObjectAssignment.objects.filter(project_id=1).count()

        self._add(2)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=1).count(), before)

    def test_linking_the_same_customer_twice_still_lists_them_once(self):
        self._add(2)
        self.assertEqual(self._add(2).status_code, 201)

        self.assertEqual(self._ids(), [1, 2])

    def test_bad_customers_are_rejected_and_nothing_is_linked(self):
        Customer.objects.filter(pk=2).update(is_deleted=True)
        bodies = {"unknown": {"id": 9999}, "deleted": {"id": 2}, "missing": {}, "not a number": {"id": "abc"}}
        before = ObjectAssignment.objects.filter(project_id=2).count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(CUSTOMER_URL, body, format="json").status_code, 400)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=2).count(), before)

    def test_linking_missing_project_is_not_found(self):
        self.assertEqual(self.client.post("/api/v1/project/9999/customer/", {"id": 2}, format="json").status_code, 404)

    # ---------- unlink ----------
    def test_unlinking_a_customer(self):
        response = self.client.delete(f"{CUSTOMER_URL}1/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self._ids(), [])

    def test_unlinking_is_a_soft_delete(self):
        self.client.delete(f"{CUSTOMER_URL}1/")

        row = self._rows(1).get()
        self.assertTrue(row.is_deleted)
        self.assertEqual(row.change_user, self.leader)

    def test_unlinking_leaves_other_projects_alone(self):
        self.client.delete(f"{CUSTOMER_URL}1/")

        self.assertFalse(self._rows(1, project_id=1).get().is_deleted)

    def test_unlinking_removes_every_link_when_a_customer_was_linked_twice(self):
        self._add(2)
        self._add(2)

        self.assertEqual(self.client.delete(f"{CUSTOMER_URL}2/").status_code, 204)

        self.assertEqual(self._ids(), [1])
        self.assertFalse(self._rows(2).filter(is_deleted=False).exists())

    def test_unlinking_a_customer_that_is_not_linked_is_rejected(self):
        self.assertEqual(self.client.delete(f"{CUSTOMER_URL}2/").status_code, 400)

    def test_unlinking_twice_is_rejected(self):
        self.client.delete(f"{CUSTOMER_URL}1/")

        self.assertEqual(self.client.delete(f"{CUSTOMER_URL}1/").status_code, 400)

    def test_a_customer_can_be_linked_again_after_unlinking(self):
        self.client.delete(f"{CUSTOMER_URL}1/")

        self.assertEqual(self._add(1).status_code, 201)
        self.assertEqual(self._ids(), [1])

    def test_unlinking_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete("/api/v1/project/9999/customer/1/").status_code, 404)


class ProjectOrganisationTests(TeamLeaderProjectBase):
    def setUp(self):
        super().setUp()
        self.second_org = Organisation.objects.create(
            name="Second Organisation", creation_user=self.admin, change_user=self.admin
        )

    def _set(self, organisation_id):
        return self.client.post(ORGANISATION_URL, {"id": organisation_id}, format="json")

    @staticmethod
    def _organisation_id():
        return Project.objects.get(pk=2).organisation_id

    # ---------- read ----------
    def test_get_has_the_organisation_its_customers_and_the_choices(self):
        response = self.client.get(ORGANISATION_URL)

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["organisation"]["id"], 1)
        self.assertEqual([c["id"] for c in response.data["customers"]], [1])
        self.assertEqual(sorted(c["id"] for c in response.data["potential_customers"]), [1, 2])
        self.assertEqual(sorted(o["id"] for o in response.data["potential_organisations"]), [1, self.second_org.pk])

    def test_potential_organisations_are_sorted_by_name_and_skip_deleted(self):
        Organisation.objects.create(name="Deleted", is_deleted=True, creation_user=self.admin, change_user=self.admin)

        names = [o["name"] for o in self.client.get(ORGANISATION_URL).data["potential_organisations"]]

        self.assertEqual(names, ["NearBeach Incorporate", "Second Organisation"])

    def test_get_for_a_project_without_an_organisation(self):
        project = self._make_project("No organisation")

        response = self.client.get(f"/api/v1/project/{project.pk}/organisation/")

        self.assertEqual(response.status_code, 200, response.data)
        for key in ("organisation", "customers", "potential_customers"):
            self.assertIsNone(response.data[key])
        self.assertEqual(len(response.data["potential_organisations"]), 2)

    def test_get_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/organisation/").status_code, 404)

    # ---------- set ----------
    def test_setting_the_organisation(self):
        response = self._set(self.second_org.pk)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["organisation"]["id"], self.second_org.pk)
        self.assertEqual(self._organisation_id(), self.second_org.pk)

    def test_setting_the_organisation_sends_back_its_customers(self):
        Customer.objects.filter(pk=2).update(organisation=self.second_org)

        response = self._set(self.second_org.pk)

        self.assertEqual([c["id"] for c in response.data["potential_customers"]], [2])

    def test_setting_the_organisation_does_not_change_other_projects(self):
        self._set(self.second_org.pk)

        self.assertEqual(Project.objects.get(pk=1).organisation_id, 1)

    def test_the_new_organisation_shows_in_the_project(self):
        self._set(self.second_org.pk)

        self.assertEqual(self.client.get(QA_PROJECT_URL).data["organisation"]["id"], self.second_org.pk)

    def test_bad_organisations_are_rejected_and_nothing_changes(self):
        self.second_org.is_deleted = True
        self.second_org.save()
        bodies = {"unknown": {"id": 9999}, "deleted": {"id": self.second_org.pk}, "missing": {}, "not a number": {"id": "abc"}}

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(ORGANISATION_URL, body, format="json").status_code, 400)

        self.assertEqual(self._organisation_id(), 1)

    def test_setting_on_a_missing_project_is_not_found(self):
        self.assertEqual(self.client.post("/api/v1/project/9999/organisation/", {"id": 1}, format="json").status_code, 404)

    # ---------- remove ----------
    def test_removing_the_organisation(self):
        response = self.client.delete(ORGANISATION_URL)

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self._organisation_id())

    def test_removing_the_organisation_records_who_did_it(self):
        self.client.delete(ORGANISATION_URL)

        self.assertEqual(Project.objects.get(pk=2).change_user, self.leader)

    def test_removing_the_organisation_keeps_the_linked_customers(self):
        self.client.delete(ORGANISATION_URL)

        self.assertEqual([c["id"] for c in self.client.get(CUSTOMER_URL).data], [1])

    def test_removing_the_organisation_does_not_change_other_projects(self):
        self.client.delete(ORGANISATION_URL)

        self.assertEqual(Project.objects.get(pk=1).organisation_id, 1)

    def test_removing_when_there_is_no_organisation_still_succeeds(self):
        self.client.delete(ORGANISATION_URL)

        self.assertEqual(self.client.delete(ORGANISATION_URL).status_code, 204)

    def test_removing_from_a_missing_project_is_not_found(self):
        self.assertEqual(self.client.delete("/api/v1/project/9999/organisation/").status_code, 404)
