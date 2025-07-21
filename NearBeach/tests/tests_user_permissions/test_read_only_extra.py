from collections import namedtuple
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "read_only_extra"
password = "Test1234$"


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class ReadOnlyPermissionTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {
            "two_factor_login_view-current_step": "auth",
            "auth-username": username,
            "auth-password": password
        }

        # Setup the client
        self.client = Client()

        login_user(self.client, self)

    def test_basic_page_loads_successful(self):
        """
        The following tests will make sure the read only can access most pages on the
        system.
        """
        URLTest = namedtuple(
            "URLTest",
            ["url", "args", "data", "status_code", "method"],
            defaults=["", [], {}, 200, "GET"],
        )

        data_list = [
            URLTest("dashboard", [], {}, 200, "GET"),
            URLTest("change_task_information", [2], {}, 200, "GET"),
            URLTest("customer_information", [1], {}, 200, "GET"),
            URLTest("kanban_information", [2], {}, 200, "GET"),
            URLTest("permission_set_information", [2], {}, 403, "GET"),
            URLTest("profile_information", [], {}, 200, "GET"),
            URLTest("new_customer", [], {}, 403, "GET"),
            URLTest("new_group", [], {}, 403, "GET"),
            URLTest("new_kanban", [], {}, 403, "GET"),
            URLTest("new_organisation", [], {}, 403, "GET"),
            URLTest("new_permission_set", [], {}, 403, "GET"),
            URLTest("new_project", [], {}, 403, "GET"),
            URLTest("new_request_for_change", [], {}, 403, "GET"),
            URLTest("new_requirement", [], {}, 403, "GET"),
            URLTest("new_task", [], {}, 403, "GET"),
            URLTest("new_user", [], {}, 403, "GET"),
            URLTest("organisation_information", [1], {}, 200, "GET"),
            URLTest("project_information", [2], {}, 200, "GET"),
            URLTest("requirement_information", [2], {}, 200, "GET"),
            URLTest("requirement_item_information", [2], {}, 200, "GET"),
            URLTest("rfc_information", [2], {}, 200, "GET"),
            URLTest("rfc_readonly", [2], {}, 200, "GET"),
            URLTest("search", [], {}, 200, "GET"),
            URLTest("search_group", [], {}, 403, "GET"),
            URLTest("search_customer", [], {}, 200, "GET"),
            URLTest("search_organisation", [], {}, 200, "GET"),
            URLTest("search_permission_set", [], {}, 403, "GET"),
            URLTest("search_tag", [], {}, 200, "GET"),
            URLTest("search_user", [], {}, 403, "GET"),
            URLTest("task_information", [2], {}, 200, "GET"),
            URLTest("change_task_information", [1], {}, 403, "GET"),
            URLTest("kanban_information", [1], {}, 403, "GET"),
            URLTest("permission_set_information", [1], {}, 403, "GET"),
            URLTest("project_information", [1], {}, 403, "GET"),
            URLTest("requirement_information", [1], {}, 403, "GET"),
            URLTest("requirement_item_information", [1], {}, 403, "GET"),
            URLTest("rfc_information", [1], {}, 403, "GET"),
            URLTest("rfc_readonly", [1], {}, 403, "GET"),
            URLTest("task_information", [1], {}, 403, "GET"),
            URLTest("user_information", [1], {}, 403, "GET"),
            URLTest("add_customer", ["project", 2], {"customer": 1}, 403, "POST"),
            URLTest("private_download_file", ["80a7bd50-eba9-49f8-a55c-d1febd052ab9"], {}, 400, "GET"),
            URLTest("my_planner", [], {}, 200, "GET"),
            URLTest("my_planner_add_object", [], {"job_date": "2024-05-14", "destination": "task", "task": 1}, 200, "POST"),
            URLTest("my_planner_delete_user_job", [], {"user_job_id": 1}, 400, "POST"),
            URLTest("my_planner_delete_user_job", [], {"user_job_id": 5}, 200, "POST"),
            URLTest("my_planner_get_object_list", ["project"], {}, 200, "POST"),
            URLTest("my_planner_get_object_list", ["task"], {}, 200, "POST"),
            URLTest("my_planner_update_object_list", [], {"user_job_id": 1, "job_date": "2024-05-15", "new_destination": 1}, 400, "POST"),
            URLTest("my_planner_update_object_list", [], {"user_job_id": 5, "job_date": "2024-05-15", "new_destination": 3}, 200, "POST"),
            URLTest("sprint_information", [1], {}, 403, "GET"),
            URLTest("sprint_information", [2], {}, 200, "GET"),
            URLTest("sprint_information", [3], {}, 403, "GET"),
            URLTest("sprint_information", [4], {}, 200, "GET"),
            URLTest("gantt_chart_get_data", ["sprint", 1], {}, 403, "GET"),
            URLTest("gantt_chart_get_data", ["sprint", 2], {}, 200, "GET"),
            URLTest("gantt_chart_get_data", ["sprint", 3], {}, 403, "GET"),
            URLTest("gantt_chart_get_data", ["sprint", 4], {}, 200, "GET"),
            URLTest("gantt_chart_get_data", ["project", 3], {}, 403, "GET"),
            URLTest("gantt_chart_update_data", ["project", 1], {"end_date": "2024-05-10", "start_date": "2024-05-01", "status_id": 1}, 403, "POST"),
            URLTest("gantt_chart_update_data", ["project", 2], {"end_date": "2024-05-10", "start_date": "2024-05-01", "status_id": 1}, 403, "POST"),
            URLTest("gantt_chart_update_data", ["task", 1], {"end_date": "2024-05-10", "start_date": "2024-05-01", "status_id": 1}, 403, "POST"),
            URLTest("gantt_chart_update_data", ["task", 2], {"end_date": "2024-05-10", "start_date": "2024-05-01", "status_id": 1}, 403, "POST"),
            URLTest("add_notes", ["project", 1], {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z", "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "", "can_edit": "true"}, 403, "POST"),
            URLTest("add_notes", ["project", 2], {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z", "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "", "can_edit": "true"}, 200, "POST"),
            URLTest("add_notes", ["task", 1],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 403, "POST"),
            URLTest("add_notes", ["task", 2],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 200, "POST"),
            URLTest("organisation_add_notes", ["organisation", 1],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 200, "POST"),
            URLTest("add_notes", ["kanban_card", 1],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 403, "POST"),
            URLTest("add_notes", ["kanban_card", 2],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 200, "POST"),
            URLTest("add_notes", ["requirement", 1],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 403, "POST"),
            URLTest("add_notes", ["requirement", 2],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 200, "POST"),
            URLTest("add_notes", ["requirement_item", 1],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 403, "POST"),
            URLTest("add_notes", ["requirement_item", 2],
                    {"object_note_id": 4, "object_note": "<p>Add note</p>", "date_modified": "2024-09-25T09:15:34.033Z",
                     "username": 7, "first_name": "Dark", "last_name": "Admin", "profile_picture": "",
                     "can_edit": "true"}, 200, "POST"),
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                if data.method == "GET":
                    response = self.client.get(
                        reverse(data.url, args=data.args), data.data, follow=True
                    )
                else:
                    response = self.client.post(
                        reverse(data.url, args=data.args), data.data, follow=True
                    )

                self.assertEqual(response.status_code, data.status_code)

    def test_notification_pages_redirect_to_dashboard(self):
        """
        The following tests will make sure the read only user can not access the notifications pages.
        The following uses a named tuple to shorten the tests.
        """
        URLTest = namedtuple(
            "URLTest",
            ["url","expected_url", "args", "data", "status_code", "target_status_code", "method"],
            defaults=["","", [], {}, 302, 200, "GET"],
        )

        data_list = [
            URLTest("search_notification", "/", [], {}, 302, 200, "GET"),
            URLTest("new_notification", "/", [], {}, 302, 200, "GET"),
            URLTest("notification_information", "/", [1], {}, 302, 200, "GET"),
            URLTest("diagnostic_information_email_test", "/", [], {}, 302, 200, "POST"),
            URLTest("diagnostic_information", "/", [], {}, 302, 200, "GET"),
            URLTest("diagnostic_information_upload_test", "/", [], {}, 302, 200, "POST"),
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                if data.method == "GET":
                    response = self.client.get(
                        reverse(data.url, args=data.args), data.data, follow=True
                    )
                else:
                    response = self.client.post(
                        reverse(data.url, args=data.args), data.data, follow=True
                    )

                self.assertRedirects(
                    response,
                    expected_url=data.expected_url,
                    status_code=data.status_code,
                    target_status_code=data.target_status_code,
                    fetch_redirect_response=True
                )
