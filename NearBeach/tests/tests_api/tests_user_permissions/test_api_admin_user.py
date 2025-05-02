from collections import namedtuple

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

import uuid

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


class ApiAdminPermissionTests(APITestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {
            "two_factor_login_view-current_step": "auth",
            "auth-username": username,
            "auth-password": password
        }

        # Setup the client
        self.client = APIClient()
        self.factory = APIRequestFactory()

        login_user(self.client, self)

    def test_create_account(self):
        """
        The following tests will make sure the admin can access all API points on the system
        """
        URLTest = namedtuple(
            "URLTest",
            ["url", "data", "status_code", "method"],
            defaults=["", {}, 200, "GET"],
        )

        data_list = [
            ################
            # AVAILABLE DATA
            ################
            URLTest("/api/v0/available_data/customer_list/", {"destination": "project", "location_id": 1}, 200, "GET"),
            URLTest("/api/v0/available_data/customer_list", {"destination": "project", "location_id": 1}, 301, "GET"),
            URLTest("/api/v0/available_data/customer_list/", {}, 400, "GET"),
            URLTest("/api/v0/available_data/customer_list/", {"destination": "project", "location_id": 1}, 405, "POST"),
            URLTest("/api/v0/available_data/sprint_list/", {}, 200, "GET"),
            URLTest("/api/v0/available_data/sprint_list", {"destination": "project", "location_id": 1}, 301, "GET"),
            URLTest("/api/v0/available_data/sprint_list/", {}, 405, "POST"),
            URLTest("/api/v0/available_data/tag_list/", {}, 200, "GET"),
            URLTest("/api/v0/available_data/tag_list", {"destination": "project", "location_id": 1}, 301, "GET"),
            URLTest("/api/v0/available_data/tag_list/", {}, 405, "POST"),
            ########
            # COFFEE
            ########
            URLTest("/api/v0/coffee/", {}, 418, "GET"),
            URLTest("/api/v0/coffee/", {}, 418, "POST"),
            URLTest("/api/v0/coffee/1/", {}, 418, "GET"),
            URLTest("/api/v0/coffee/1/", {}, 418, "PUT"),
            URLTest("/api/v0/coffee/1/", {}, 418, "DELETE"),
            URLTest("/api/v0/coffee", {}, 301, "GET"),
            URLTest("/api/v0/coffee", {}, 301, "POST"),
            URLTest("/api/v0/coffee/1", {}, 301, "GET"),
            URLTest("/api/v0/coffee/1", {}, 301, "PUT"),
            URLTest("/api/v0/coffee/1", {}, 301, "DELETE"),
            ##########
            # CUSTOMER
            ##########
            URLTest("/api/v0/customer/", {}, 200, "GET"),
            URLTest(
                "/api/v0/customer/",
                {
                    "customer_title": 2,
                    "customer_first_name": "Socks",
                    "customer_last_name": "Fluffy Butt",
                    "customer_email": "sock@nearbeach.org",
                    "organisation": 1
                },
                201,
                "POST"
            ),
            URLTest("/api/v0/customer/1/", {}, 200, "GET"),
            URLTest(
                "/api/v0/customer/1/",
                {
                    "customer_title": 2,
                    "customer_first_name": "Socks",
                    "customer_last_name": "Fluffy Butt",
                    "customer_email": "sock@nearbeach.org",
                },
                200,
                "PUT"
            ),
            URLTest("/api/v0/customer/1/", {}, 200, "DELETE"),
            URLTest("/api/v0/customer", {}, 301, "GET"),
            URLTest("/api/v0/customer", {}, 301, "POST"),
            URLTest("/api/v0/customer/1", {}, 301, "GET"),
            URLTest("/api/v0/customer/1", {}, 301, "PUT"),
            URLTest("/api/v0/customer/1", {}, 301, "DELETE"),
            ##############
            # KANBAN BOARD
            ##############
            URLTest("/api/v0/kanban_board/", {}, 200, "GET"),
            URLTest(
                "/api/v0/kanban_board/",
                {
                    "kanban_board_name": "API Kanban Board - " + str(uuid.uuid4()),
                    "group_list": 1,
                    "group_list": 2,
                    "column_title": "Backlog",
                    "column_property": "Normal",
                    "column_title": "In Progress",
                    "column_property": "Normal",
                    "column_title": "Blocked",
                    "column_property": "Blocked",
                    "column_title": "Review and QA",
                    "column_property": "Normal",
                    "column_title": "Completed",
                    "column_property": "Closed",
                    "level_title": "Swim Lane 1",
                    "level_title": "Swim Lane 2",
                },
                201,
                "POST"
            ),
            URLTest("/api/v0/kanban_board/1/", {}, 200, "GET"),
            URLTest("/api/v0/kanban_board/2/", {}, 200, "GET"),
            URLTest("/api/v0/kanban_board/1/", {}, 200, "DELETE"),
            URLTest("/api/v0/kanban_board/2/", {}, 200, "DELETE"),
            URLTest("/api/v0/kanban_board", {}, 301, "GET"),
            URLTest("/api/v0/kanban_board", {}, 301, "POST"),
            URLTest("/api/v0/kanban_board/1", {}, 301, "GET"),
            URLTest("/api/v0/kanban_board/2", {}, 301, "GET"),
            URLTest("/api/v0/kanban_board/1", {}, 301, "PUT"),
            URLTest("/api/v0/kanban_board/2", {}, 301, "PUT"),
            URLTest("/api/v0/kanban_board/1", {}, 301, "DELETE"),
            URLTest("/api/v0/kanban_board/2", {}, 301, "DELETE"),
            URLTest("/api/v0/kanban_board/1/group_and_user/", {}, 200, "GET"),
            URLTest("/api/v0/kanban_board/1/group_and_user/", {"group_list": 2, "user_list": 2}, 201, "POST"),
            URLTest(
                "/api/v0/kanban_board/1/group_and_user/0/",
                {
                    "user": 2,
                },
                200,
                "DELETE"
            ),
            URLTest(
                "/api/v0/kanban_board/1/group_and_user/0/",
                {
                    "group": 2,
                },
                200,
                "DELETE"
            ),
            URLTest(
                "/api/v0/kanban_board/1/group_and_user/0/",
                {
                    "group": 1,
                },
                403,
                "DELETE"
            ),
            URLTest("/api/v0/kanban_board/2/group_and_user/", {}, 200, "GET"),
            URLTest("/api/v0/kanban_board/2/group_and_user/", {"group_list": 3}, 201, "POST"),
            URLTest(
                "/api/v0/kanban_board/2/group_and_user/0/",
                {
                    "user": 2,
                },
                200,
                "DELETE"
            ),
            URLTest(
                "/api/v0/kanban_board/2/group_and_user/0/",
                {
                    "group": 1,
                },
                200,
                "DELETE"
            ),
            ##############
            # ORGANISATION
            ##############
            URLTest("/api/v0/organisation/", {}, 200, "GET"),
            URLTest(
                "/api/v0/organisation/",
                {
                    "organisation_name": "Far Desert",
                    "organisation_email": "support@fardesert.com",
                    "organisation_website": "https://fardesert.com",
                },
                201,
                "POST"
            ),
            URLTest("/api/v0/organisation/1/", {}, 200, "GET"),
            URLTest(
                "/api/v0/organisation/1/",
                {
                    "organisation_name": "Far Desert",
                    "organisation_email": "support@fardesert.com",
                    "organisation_website": "https://fardesert.com",
                },
                200,
                "PUT"
            ),
            URLTest("/api/v0/organisation/1/", {}, 200, "DELETE"),
            URLTest("/api/v0/organisation", {}, 301, "GET"),
            URLTest("/api/v0/organisation", {}, 301, "POST"),
            URLTest("/api/v0/organisation/1", {}, 301, "GET"),
            URLTest("/api/v0/organisation/1", {}, 301, "PUT"),
            URLTest("/api/v0/organisation/1", {}, 301, "DELETE"),
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                if data.method == "GET":
                    response = self.client.get(
                        data.url,
                        data.data,
                    )
                elif data.method == "POST":
                    response = self.client.post(
                        data.url,
                        data.data,
                    )
                elif data.method == "PUT":
                    response = self.client.put(
                        data.url,
                        data.data,
                        format="json"
                    )
                elif data.method == "DELETE":
                    response = self.client.delete(
                        data.url,
                        data.data,
                        format="json"
                    )
                else:
                    AssertionError("Method Not allowed in API")

                self.assertEqual(response.status_code, data.status_code)
