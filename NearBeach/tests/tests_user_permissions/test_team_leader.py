from collections import namedtuple
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "team_leader"
password = "Test1234$"


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class TeamLeaderPermissionTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {"username": username, "password": password}

        # Setup the client
        self.client = Client()

        login_user(self.client, self)

    def test_basic_page_loads_successful(self):
        """
        The following tests will make sure the team leader can access most pages on the
        system. This is only testing pages they can LAND on.
        """
        URLTest = namedtuple(
            "URLTest",
            ["url", "args", "data", "status_code", "method"],
            defaults=["", [], {}, 200, "GET"],
        )

        data_list = [
            URLTest("dashboard", [], {}, 200),
            URLTest("change_task_information", [2], {}, 200),
            URLTest("customer_information", [1], {}, 200),
            URLTest("kanban_information", [2], {}, 200),
            URLTest("permission_set_information", [2], {}, 403),
            URLTest("profile_information", [], {}, 200),
            URLTest("new_customer", [], {}, 200),
            URLTest("new_group", [], {}, 403),
            URLTest("new_kanban", [], {}, 200),
            URLTest("new_organisation", [], {}, 200),
            URLTest("new_permission_set", [], {}, 403),
            URLTest("new_project", [], {}, 200),
            URLTest("new_request_for_change", [], {}, 200),
            URLTest("new_requirement", [], {}, 200),
            URLTest("new_task", [], {}, 200),
            URLTest("new_user", [], {}, 403),
            URLTest("organisation_information", [1], {}, 200),
            URLTest("project_information", [2], {}, 200),
            URLTest("requirement_information", [2], {}, 200),
            URLTest("requirement_item_information", [2], {}, 200),
            URLTest("rfc_information", [2], {}, 200),
            URLTest("rfc_readonly", [2], {}, 200),
            URLTest("search", [], {}, 200),
            URLTest("search_group", [], {}, 403),
            URLTest("search_customer", [], {}, 200),
            URLTest("search_organisation", [], {}, 200),
            URLTest("search_permission_set", [], {}, 403),
            URLTest("search_tag", [], {}, 200),
            URLTest("search_user", [], {}, 403),
            URLTest("task_information", [2], {}, 200),
            URLTest("change_task_information", [1], {}, 403),
            URLTest("kanban_information", [1], {}, 403),
            URLTest("permission_set_information", [1], {}, 403),
            URLTest("project_information", [1], {}, 403),
            URLTest("requirement_information", [1], {}, 403),
            URLTest("requirement_item_information", [1], {}, 403),
            URLTest("rfc_information", [1], {}, 403),
            URLTest("rfc_readonly", [1], {}, 403),
            URLTest("task_information", [1], {}, 403),
            URLTest("user_information", [1], {}, 403),
            URLTest("add_customer", ["project", 2], {"customer": 1}, 200, "POST"),
            URLTest("private_download_file", ["80a7bd50-eba9-49f8-a55c-d1febd052ab9"], {}, 400),
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
        The following tests will make sure the team leader can not access the notifications pages.
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
