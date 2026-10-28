"""CRUD tests for the project endpoints, run as the team leader.

The permission tests (tests_permissions) only check status codes. These check what a request really does -
the response body and the rows left in the database.

The team leader is in the "QA Team" group (2) only, with full permission on projects. In the fixture they can
see project 2 ("Project - QA Team") but not project 1, which belongs to the Administration group (1).
"""
from datetime import datetime, timezone

from django.contrib.auth import get_user_model

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.project import ListOfProjectStatus, Project
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

PROJECT_LIST_URL = "/api/v1/project/"
QA_PROJECT_URL = "/api/v1/project/2/"

# Fixture ids
ADMIN_GROUP = 1
QA_GROUP = 2
EMPTY_GROUP = 3
CLOSED_STATUS = 6


class TeamLeaderProjectBase(BaseApiClass):
    username = "team_leader"
    password = "Test1234$"

    @property
    def leader(self):
        return get_user_model().objects.get(username="team_leader")

    @property
    def admin(self):
        return get_user_model().objects.get(username="admin")

    def _create_project(self, **overrides):
        """Create a project through the API as the team leader - returns the response"""
        body = {"title": "Leader project", "group_list": [QA_GROUP], **overrides}
        return self.client.post(PROJECT_LIST_URL, body, format="json")

    def _make_project(self, title, groups=(QA_GROUP,), **fields):
        """Create a project straight in the database - for data the team leader should (or should not) see"""
        project = Project.objects.create(
            title=title,
            status=ListOfProjectStatus.objects.get(pk=fields.pop("status_id", 1)),
            creation_user=self.admin,
            change_user=self.admin,
            **fields,
        )
        for group_id in groups:
            ObjectAssignment.objects.create(
                project=project,
                group_id=group_id,
                creation_user=self.admin,
                change_user=self.admin,
            )
        return project


class ProjectCreateTests(TeamLeaderProjectBase):
    def test_create_saves_the_fields_that_were_sent(self):
        response = self._create_project(
            title="Fully specified",
            description="<p>Everything filled in</p>",
            priority=1,
            story_point=5,
            start_date="2026-03-01T09:00:00Z",
            end_date="2026-03-15T17:00:00Z",
        )

        self.assertEqual(response.status_code, 201, response.data)
        project = Project.objects.get(pk=response.data["id"])
        self.assertEqual(project.title, "Fully specified")
        self.assertEqual(project.description, "<p>Everything filled in</p>")
        self.assertEqual(project.priority, 1)
        self.assertEqual(project.story_point, 5)
        self.assertEqual(project.start_date, datetime(2026, 3, 1, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(project.end_date, datetime(2026, 3, 15, 17, 0, tzinfo=timezone.utc))

    def test_create_response_describes_the_new_project(self):
        response = self._create_project(title="Response check")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["title"], "Response check")
        self.assertEqual(response.data["id"], Project.objects.get(title="Response check").pk)
        self.assertEqual(response.data["status"]["status"], "New")
        self.assertEqual(response.data["priority"], {"value": 2, "label": "Normal"})
        self.assertIsNone(response.data["organisation"])

    def test_create_uses_defaults_for_what_was_left_out(self):
        response = self._create_project(title="Bare minimum")

        project = Project.objects.get(pk=response.data["id"])
        self.assertEqual(project.description, "")
        self.assertEqual(project.priority, 2)
        self.assertEqual(project.story_point, 1)
        self.assertIsNone(project.organisation)

    def test_create_records_the_team_leader_as_creator(self):
        response = self._create_project()

        project = Project.objects.get(pk=response.data["id"])
        self.assertEqual(project.creation_user, self.leader)
        self.assertEqual(project.change_user, self.leader)
        self.assertFalse(project.is_deleted)

    def test_create_starts_in_the_first_status_by_sort_order(self):
        """The first status that has not been deleted - whatever its id is"""
        ListOfProjectStatus.objects.create(
            status="Triage", sort_order=0, creation_user=self.admin, change_user=self.admin,
        )
        ListOfProjectStatus.objects.create(
            status="Retired", sort_order=0, is_deleted=True, creation_user=self.admin, change_user=self.admin,
        )

        response = self._create_project()

        self.assertEqual(response.data["status"]["status"], "Triage")
        self.assertEqual(Project.objects.get(pk=response.data["id"]).status.status, "Triage")

    def test_create_assigns_the_project_to_the_group(self):
        response = self._create_project()

        assignments = ObjectAssignment.objects.filter(project_id=response.data["id"], is_deleted=False)
        self.assertEqual(assignments.count(), 1)
        assignment = assignments.get()
        self.assertEqual(assignment.group_id, QA_GROUP)
        self.assertEqual(assignment.creation_user, self.leader)
        self.assertEqual(assignment.change_user, self.leader)

    def test_create_requires_a_title(self):
        before = Project.objects.count()

        for name, body in {
            "missing": {"group_list": [QA_GROUP]},
            "blank": {"title": "", "group_list": [QA_GROUP]},
            "too long": {"title": "x" * 256, "group_list": [QA_GROUP]},
        }.items():
            with self.subTest(name):
                response = self.client.post(PROJECT_LIST_URL, body, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn("title", response.data)

        self.assertEqual(Project.objects.count(), before)

    def test_create_rejects_groups_the_team_leader_is_not_in(self):
        before_projects = Project.objects.count()
        before_assignments = ObjectAssignment.objects.count()

        for group_id in (ADMIN_GROUP, EMPTY_GROUP):
            with self.subTest(group=group_id):
                response = self._create_project(group_list=[group_id])
                self.assertEqual(response.status_code, 400)

        self.assertEqual(Project.objects.count(), before_projects)
        self.assertEqual(ObjectAssignment.objects.count(), before_assignments)

    def test_create_rejects_invalid_values(self):
        before = Project.objects.count()

        for name, change in {
            "priority out of range": {"priority": 9},
            "priority not a number": {"priority": "urgent"},
            "story points not a number": {"story_point": "lots"},
            "start date not a date": {"start_date": "next week"},
            "group that does not exist": {"group_list": [9999]},
        }.items():
            with self.subTest(name):
                response = self._create_project(**change)
                self.assertEqual(response.status_code, 400, response.data)

        self.assertEqual(Project.objects.count(), before)

    def test_a_created_project_can_be_read_back(self):
        created = self._create_project(title="Round trip")

        retrieved = self.client.get(f"{PROJECT_LIST_URL}{created.data['id']}/")

        self.assertEqual(retrieved.status_code, 200)
        self.assertEqual(retrieved.data["title"], "Round trip")
        self.assertEqual([group["id"] for group in retrieved.data["group_list"]], [QA_GROUP])


class ProjectListTests(TeamLeaderProjectBase):
    def _titles(self, query=""):
        response = self.client.get(f"{PROJECT_LIST_URL}{query}")
        self.assertEqual(response.status_code, 200, response.data)
        return [row["title"] for row in response.data["results"]]

    def test_list_is_paginated(self):
        response = self.client.get(PROJECT_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertEqual(response.data["count"], len(response.data["results"]))
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_list_rows_have_the_project_fields(self):
        row = self.client.get(PROJECT_LIST_URL).data["results"][0]

        self.assertEqual(
            set(row),
            {
                "id", "title", "description", "organisation", "status", "priority", "story_point",
                "start_date", "end_date", "date_created", "date_modified",
            },
        )

    def test_list_only_has_projects_in_the_leaders_groups(self):
        self._make_project("Admin only", groups=(ADMIN_GROUP,))
        self._make_project("Both groups", groups=(ADMIN_GROUP, QA_GROUP))
        self._make_project("Empty group only", groups=(EMPTY_GROUP,))

        titles = self._titles()

        self.assertIn("Project - QA Team", titles)
        self.assertIn("Both groups", titles)
        self.assertNotIn("Project - Only Administration", titles)
        self.assertNotIn("Admin only", titles)
        self.assertNotIn("Empty group only", titles)

    def test_list_shows_a_project_only_once_when_it_has_several_groups(self):
        self._make_project("Two assignments", groups=(QA_GROUP, QA_GROUP))

        self.assertEqual(self._titles().count("Two assignments"), 1)

    def test_list_has_projects_the_leader_creates(self):
        self._create_project(title="Brand new")

        self.assertIn("Brand new", self._titles())

    def test_list_leaves_out_deleted_projects(self):
        self._make_project("Deleted one", is_deleted=True)

        self.assertNotIn("Deleted one", self._titles())

    def test_list_leaves_out_projects_whose_assignment_was_removed(self):
        project = self._make_project("Unassigned later")
        ObjectAssignment.objects.filter(project=project).update(is_deleted=True)

        self.assertNotIn("Unassigned later", self._titles())

    def test_search_matches_part_of_a_title_ignoring_case(self):
        self._make_project("Quarterly Planning")
        self._make_project("Annual report")

        self.assertEqual(self._titles("?search=quarter"), ["Quarterly Planning"])
        self.assertEqual(self._titles("?search=PLANNING"), ["Quarterly Planning"])

    def test_search_matches_an_id(self):
        self.assertEqual(self._titles("?search=2"), ["Project - QA Team"])

    def test_search_with_no_matches_gives_an_empty_page(self):
        response = self.client.get(f"{PROJECT_LIST_URL}?search=nothing-like-this")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_closed_projects_are_hidden_unless_asked_for(self):
        self._make_project("Finished work", status_id=CLOSED_STATUS)

        self.assertNotIn("Finished work", self._titles())
        self.assertNotIn("Finished work", self._titles("?show_closed=false"))
        self.assertIn("Finished work", self._titles("?show_closed=true"))

    def test_show_closed_still_includes_open_projects(self):
        self._make_project("Finished work", status_id=CLOSED_STATUS)

        titles = self._titles("?show_closed=true")

        self.assertIn("Project - QA Team", titles)
        self.assertIn("Finished work", titles)


class ProjectRetrieveTests(TeamLeaderProjectBase):
    def test_retrieve_returns_the_project_fields(self):
        response = self.client.get(QA_PROJECT_URL)

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data["id"], 2)
        self.assertEqual(data["title"], "Project - QA Team")
        self.assertEqual(data["description"], "<p>Project - QA Team</p>")
        self.assertEqual(data["story_point"], 1)
        self.assertEqual(data["priority"], {"value": 2, "label": "Normal"})
        self.assertEqual(data["status"]["id"], 1)
        self.assertEqual(data["status"]["status"], "New")
        self.assertEqual(data["start_date"], "2023-02-14T22:00:00Z")
        self.assertEqual(data["end_date"], "2023-03-01T05:00:00Z")
        self.assertEqual(data["organisation"]["id"], 1)

    def test_retrieve_lists_the_groups_on_the_project(self):
        groups = self.client.get(QA_PROJECT_URL).data["group_list"]

        self.assertEqual([group["id"] for group in groups], [QA_GROUP])
        self.assertEqual(groups[0]["name"], "QA Team")

    def test_retrieve_lists_the_users_on_the_project(self):
        users = self.client.get(QA_PROJECT_URL).data["user_list"]

        self.assertEqual(sorted(user["username"] for user in users), ["read_only", "team_leader"])
        for user in users:
            with self.subTest(user=user["username"]):
                self.assertEqual(user["full_name"], f'{user["first_name"]} {user["last_name"]}')

    def test_retrieve_follows_changes_made_to_the_project(self):
        project = self._make_project("Before")
        Project.objects.filter(pk=project.pk).update(title="After")

        self.assertEqual(self.client.get(f"{PROJECT_LIST_URL}{project.pk}/").data["title"], "After")

    def test_retrieve_leaves_out_groups_that_were_removed(self):
        project = self._make_project("Two groups", groups=(ADMIN_GROUP, QA_GROUP))
        ObjectAssignment.objects.filter(project=project, group_id=ADMIN_GROUP).update(is_deleted=True)

        groups = self.client.get(f"{PROJECT_LIST_URL}{project.pk}/").data["group_list"]

        self.assertEqual([group["id"] for group in groups], [QA_GROUP])

    def test_a_project_that_does_not_exist_is_not_found(self):
        self.assertEqual(self.client.get(f"{PROJECT_LIST_URL}9999/").status_code, 404)

    def test_a_deleted_project_is_not_found(self):
        project = self._make_project("Gone", is_deleted=True)

        self.assertEqual(self.client.get(f"{PROJECT_LIST_URL}{project.pk}/").status_code, 404)


class ProjectUpdateTests(TeamLeaderProjectBase):
    def _patch(self, body, url=QA_PROJECT_URL):
        return self.client.patch(url, body, format="json")

    def test_patch_changes_the_title_and_description(self):
        response = self._patch({"title": "Renamed", "description": "<p>New words</p>"})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["title"], "Renamed")
        project = Project.objects.get(pk=2)
        self.assertEqual(project.title, "Renamed")
        self.assertEqual(project.description, "<p>New words</p>")

    def test_patch_only_changes_the_fields_that_were_sent(self):
        before = Project.objects.get(pk=2)

        self._patch({"title": "Only the title"})

        after = Project.objects.get(pk=2)
        self.assertEqual(after.title, "Only the title")
        self.assertEqual(after.description, before.description)
        self.assertEqual(after.priority, before.priority)
        self.assertEqual(after.story_point, before.story_point)
        self.assertEqual(after.status_id, before.status_id)
        self.assertEqual(after.start_date, before.start_date)
        self.assertEqual(after.end_date, before.end_date)

    def test_patch_changes_priority_story_points_and_dates(self):
        response = self._patch(
            {
                "priority": 0,
                "story_point": 8,
                "start_date": "2026-05-01T08:00:00Z",
                "end_date": "2026-05-09T16:00:00Z",
            }
        )

        self.assertEqual(response.status_code, 200, response.data)
        project = Project.objects.get(pk=2)
        self.assertEqual(project.priority, 0)
        self.assertEqual(project.story_point, 8)
        self.assertEqual(project.start_date, datetime(2026, 5, 1, 8, 0, tzinfo=timezone.utc))
        self.assertEqual(project.end_date, datetime(2026, 5, 9, 16, 0, tzinfo=timezone.utc))
        self.assertEqual(response.data["priority"], {"value": 0, "label": "Highest"})
        self.assertEqual(response.data["story_point"], 8)

    def test_patch_accepts_priority_as_a_value_object(self):
        """The front end sends back the {value, label} shape it was given"""
        response = self._patch({"priority": {"value": 3, "label": "Low"}})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(Project.objects.get(pk=2).priority, 3)

    def test_patch_changes_the_status_by_id(self):
        response = self._patch({"status": 4})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(Project.objects.get(pk=2).status_id, 4)
        self.assertEqual(response.data["status"], 4)

    def test_patch_rejects_a_status_that_does_not_exist_or_was_deleted(self):
        ListOfProjectStatus.objects.filter(pk=3).update(is_deleted=True)

        for status_id in (9999, 3):
            with self.subTest(status=status_id):
                response = self._patch({"status": status_id})
                self.assertEqual(response.status_code, 400)
                self.assertIn("status", response.data)

        self.assertEqual(Project.objects.get(pk=2).status_id, 1)

    def test_patch_rejects_invalid_values_and_changes_nothing(self):
        before = Project.objects.values().get(pk=2)

        for name, body in {
            "blank title": {"title": ""},
            "title too long": {"title": "x" * 256},
            "priority out of range": {"priority": 9},
            "story points not a number": {"story_point": "many"},
            "end date not a date": {"end_date": "someday"},
        }.items():
            with self.subTest(name):
                response = self._patch(body)
                self.assertEqual(response.status_code, 400, response.data)

        self.assertEqual(Project.objects.values().get(pk=2), before)

    def test_patch_ignores_groups_and_organisation(self):
        """Groups and the organisation have their own endpoints - they are not part of the PATCH shape"""
        before_title = Project.objects.get(pk=2).title

        response = self._patch({"title": before_title, "group_list": [ADMIN_GROUP], "organisation": 99})

        self.assertEqual(response.status_code, 200, response.data)
        assigned = ObjectAssignment.objects.filter(project_id=2, group__isnull=False, is_deleted=False)
        self.assertEqual(sorted(assigned.values_list("group_id", flat=True)), [QA_GROUP])
        self.assertEqual(Project.objects.get(pk=2).organisation_id, 1)

    def test_patch_does_not_touch_other_projects(self):
        other = self._make_project("Bystander")

        self._patch({"title": "Changed"})

        self.assertEqual(Project.objects.get(pk=other.pk).title, "Bystander")

    def test_patch_moves_date_modified_forward(self):
        before = Project.objects.get(pk=2).date_modified

        self._patch({"title": "Touched"})

        self.assertGreater(Project.objects.get(pk=2).date_modified, before)

    def test_patch_records_who_made_the_change(self):
        """Regression - ProjectService.update set change_user on the serializer, so it was never saved"""
        self._patch({"title": "Changed by the leader"})

        self.assertEqual(
            Project.objects.get(pk=2).change_user,
            self.leader
        )

    def test_a_project_that_does_not_exist_cannot_be_patched(self):
        self.assertEqual(self._patch({"title": "Nope"}, url=f"{PROJECT_LIST_URL}9999/").status_code, 404)

    def test_a_deleted_project_cannot_be_patched(self):
        project = self._make_project("Gone", is_deleted=True)

        response = self._patch({"title": "Back"}, url=f"{PROJECT_LIST_URL}{project.pk}/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Project.objects.get(pk=project.pk).title, "Gone")


class ProjectDeleteTests(TeamLeaderProjectBase):
    def test_delete_answers_204_with_no_body(self):
        response = self.client.delete(QA_PROJECT_URL)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(response.content)

    def test_delete_marks_the_project_deleted_instead_of_removing_it(self):
        self.client.delete(QA_PROJECT_URL)

        project = Project.objects.get(pk=2)
        self.assertTrue(project.is_deleted)
        self.assertEqual(project.title, "Project - QA Team")
        self.assertEqual(project.change_user, self.leader)

    def test_delete_keeps_the_groups_and_users_assigned_to_the_project(self):
        before = ObjectAssignment.objects.filter(project_id=2, is_deleted=False).count()

        self.client.delete(QA_PROJECT_URL)

        self.assertEqual(ObjectAssignment.objects.filter(project_id=2, is_deleted=False).count(), before)

    def test_a_deleted_project_disappears_from_the_api(self):
        self.client.delete(QA_PROJECT_URL)

        self.assertEqual(self.client.get(QA_PROJECT_URL).status_code, 404)
        self.assertEqual(self.client.patch(QA_PROJECT_URL, {"title": "x"}, format="json").status_code, 404)
        titles = [row["title"] for row in self.client.get(PROJECT_LIST_URL).data["results"]]
        self.assertNotIn("Project - QA Team", titles)
        self.assertEqual(self.client.get(f"{PROJECT_LIST_URL}?search=QA&show_closed=true").data["count"], 0)

    def test_deleting_twice_is_not_found(self):
        self.client.delete(QA_PROJECT_URL)

        self.assertEqual(self.client.delete(QA_PROJECT_URL).status_code, 404)

    def test_delete_only_removes_that_project(self):
        keep = self._create_project(title="Keeper")
        remove = self._create_project(title="Goner")

        self.client.delete(f"{PROJECT_LIST_URL}{remove.data['id']}/")

        titles = [row["title"] for row in self.client.get(PROJECT_LIST_URL).data["results"]]
        self.assertIn("Keeper", titles)
        self.assertNotIn("Goner", titles)
        self.assertFalse(Project.objects.get(pk=keep.data["id"]).is_deleted)
        self.assertFalse(Project.objects.get(pk=2).is_deleted)

    def test_a_project_that_does_not_exist_cannot_be_deleted(self):
        self.assertEqual(self.client.delete(f"{PROJECT_LIST_URL}9999/").status_code, 404)

    def test_a_project_the_leader_created_can_be_deleted(self):
        created = self._create_project(title="Short lived")

        response = self.client.delete(f"{PROJECT_LIST_URL}{created.data['id']}/")

        self.assertEqual(response.status_code, 204)
        self.assertTrue(Project.objects.get(pk=created.data["id"]).is_deleted)
