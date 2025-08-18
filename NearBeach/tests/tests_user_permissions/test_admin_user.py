from collections import namedtuple
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "admin"
password = "Test1234$"


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class AdminPermissionTests(TestCase):
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

    def test_basic_permissions_as_admin(self):
        """
        The following tests will make sure the admin can access most pages on the
        system.
        """
        URLTest = namedtuple(
            "URLTest",
            ["url", "args", "data", "status_code", "method"],
            defaults=["", [], {}, 200, "GET"],
        )

        data_list = [
            URLTest("dashboard", [], {}, 200, "GET"),
            URLTest("card_information", [1], {}, 200, "GET"),
            URLTest("change_task_information", [1], {}, 200, "GET"),
            URLTest("customer_information", [1], {}, 200, "GET"),
            URLTest("group_information", [1], {}, 200, "GET"),
            URLTest("kanban_information", [1], {}, 200, "GET"),
            URLTest("kanban_information", [1, 1], {}, 200, "GET"),
            URLTest("kanban_edit_board", [1], {}, 200, "GET"),
            URLTest("kanban_link_list", [1], {
                "array_of_objects": "project",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("kanban_link_list", [2], {
                "array_of_objects": "project",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("kanban_link_list", [1], {
                "array_of_objects": "task",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("kanban_link_list", [2], {
                "array_of_objects": "task",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("kanban_link_list", [1], {
                "array_of_objects": "requirement",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("kanban_link_list", [2], {
                "array_of_objects": "requirement",
                "destination_page": 1,
                "exclude_destination": "kanban_board",
                "exclude_location_id": 1,
                "search": "",
            }, 200, "POST"),
            URLTest("permission_set_information", [1], {}, 200, "GET"),
            URLTest("profile_information", [], {}, 200, "GET"),
            URLTest("new_group", [], {}, 200, "GET"),
            URLTest("new_kanban", [], {}, 200, "GET"),
            URLTest("new_organisation", [], {}, 200, "GET"),
            URLTest("new_permission_set", [], {}, 200, "GET"),
            URLTest("new_project", [], {}, 200, "GET"),
            URLTest("new_request_for_change", [], {}, 200, "GET"),
            URLTest("new_requirement", [], {}, 200, "GET"),
            URLTest("new_task", [], {}, 200, "GET"),
            URLTest("new_user", [], {}, 200, "GET"),
            URLTest("organisation_information", [1], {}, 200, "GET"),
            URLTest("project_information", [1], {}, 200, "GET"),
            URLTest("requirement_information", [1], {}, 200, "GET"),
            URLTest("requirement_item_information", [1], {}, 200, "GET"),
            URLTest("requirement_item_information", [1], {}, 200, "GET"),
            URLTest("rfc_information", [1], {}, 200, "GET"),
            URLTest("search", [], {}, 200, "GET"),
            URLTest("task_information", [1], {}, 200, "GET"),
            URLTest("user_information", [1], {}, 200, "GET"),
            URLTest("password_reset", [], {}, 200, "GET"),
            URLTest("object_admin_add_user", [], {"username": 2}, 200, "POST"),
            URLTest("admin_add_user", [], {"group": 1, "permission_set": 1, "username": 1}, 200, "POST"),
            URLTest("admin_add_user", [], {"group": 1, "permission_set": 1}, 400, "POST"),
            URLTest("add_customer", ["project", 1], {"customer": 1}, 200, "POST"),
            URLTest("add_group", ["project", 1], {"group_list": [1, 2]}, 200, "POST"),
            URLTest(
                "add_notes", ["project", 1], {"note": "A simple note"}, 200, "POST"
            ),
            URLTest("add_link", ["project", 1], {"project": 2, "object_relation": "blocked_by"}, 200, "POST"),
            URLTest("associated_objects", ["project", 1], {}, 200, "POST"),
            URLTest("bug_list", ["project", 1], {}, 200, "POST"),
            URLTest("customer_list", ["project", 1], {}, 200, "POST"),
            URLTest("customer_list_all", ["project", 1], {}, 200, "POST"),
            URLTest("note_list", ["project", 1], {}, 200, "POST"),
            URLTest("object_link_list", ["project", 1], {}, 200, "POST"),
            URLTest("tag_list", ["project", 1], {}, 200, "POST"),
            URLTest("user_list", ["project", 1], {}, 200, "POST"),
            URLTest("group_and_user_data", ["project", 1], {}, 200, "POST"),
            URLTest("private_download_file", ["2fc398ee-d12b-4f60-9ecb-40199ac74f13"], {}, 400, "GET"),
            URLTest("private_download_file", ["80a7bd50-eba9-49f8-a55c-d1febd052ab9"], {}, 400, "GET"),
            URLTest("new_notification", [], {}, 200, "GET"),
            URLTest("notification_information", [1], {}, 200, "GET"),
            URLTest("search_notification", [], {}, 200, "GET"),
            URLTest("update_group_leader_status", ["group"], {"group":1,"permission_set":1,"username":1,"group_leader":"true"}, 200, "POST"),
            URLTest("update_group_leader_status", ["permission_set"], {"group": 1, "permission_set": 1, "username": 1, "group_leader": "true"}, 200, "POST"),
            URLTest("update_group_leader_status", ["user"], {"group": 1, "permission_set": 1, "username": 1, "group_leader": "true"}, 200, "POST"),
            URLTest("update_group_leader_status", ["group"],
                    {"group": 1, "permission_set": 1, "username": 1, "group_leader": "false"}, 200, "POST"),
            URLTest("update_group_leader_status", ["permission_set"],
                    {"group": 1, "permission_set": 1, "username": 1, "group_leader": "false"}, 200, "POST"),
            URLTest("update_group_leader_status", ["user"],
                    {"group": 1, "permission_set": 1, "username": 1, "group_leader": "false"}, 200, "POST"),
            URLTest("update_user_password", [], {"username": 1, "password": "Test1234$"}, 200, "POST"),
            URLTest("profile_update_data", [], {"username": 1, "first_name": "Admin", "last_name": "Admin", "theme": "dark"}, 200, "POST"),
            URLTest("diagnostic_information_email_test", [], {}, 200, "POST"),
            URLTest("diagnostic_information", [], {}, 200, "GET"),
            URLTest("my_planner", [], {}, 200, "GET"),
            URLTest("my_planner_add_object", [], {"job_date": "2024-05-14", "destination": "task", "task": 1}, 200, "POST"),
            URLTest("my_planner_delete_user_job", [], {"user_job_id": 1}, 200, "POST"),
            URLTest("my_planner_get_object_list", ["project"], {}, 200, "POST"),
            URLTest("my_planner_get_object_list", ["task"], {}, 200, "POST"),
            URLTest("my_planner_update_object_list", [], {"user_job_id": 1, "job_date": "2024-05-15", "new_destination": 1}, 200, "POST"),
            URLTest("diagnostic_information_upload_test", [], {}, 200, "POST"),
            URLTest("scheduled_objects", [], {}, 200, "GET"),
            URLTest("schedule_object_information", [1], {}, 200, "GET"),
            URLTest("schedule_object_information", [3], {}, 200, "GET"),
            URLTest("schedule_object_information_save", [1], {
                "object_type": 1,
                "object_title": "trim beard",
                "object_description": "object_description",
                "object_start_date": "2024-10-17T22:00:00.000Z",
                "object_end_date": "2024-10-17T22:00:00.000Z",
                "group_list": [1,2],
                "days_before": 0,
                "number_of_repeats": -1,
                "scheduler_frequency": "Fortnightly",
                "scheduler_end_date": "2024-01-12",
                "scheduler_start_date": "2024-01-01",
                "single_day": "saturday",
                "end_date_condition": "end-date",
            }, 200, "POST"),
            URLTest("schedule_object_information_save", [3], {
                "object_type": 1,
                "object_title": "trim beard",
                "object_description": "object_description",
                "object_start_date": "2024-10-17T22:00:00.000Z",
                "object_end_date": "2024-10-17T22:00:00.000Z",
                "group_list": [1,2],
                "days_before": 0,
                "number_of_repeats": -1,
                "scheduler_frequency": "Fortnightly",
                "scheduler_end_date": "2024-01-12",
                "scheduler_start_date": "2024-01-01",
                "single_day": "saturday",
                "end_date_condition": "end-date",
            }, 200, "POST"),

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
