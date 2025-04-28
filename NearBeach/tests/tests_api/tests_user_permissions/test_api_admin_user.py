from collections import namedtuple

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

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
                    response = self.client.post(
                        data.url,
                        data.data,
                        format="json"
                    )
                elif data.method == "DELETE":
                    response = self.client.post(
                        data.url,
                        data.data,
                        format="json"
                    )
                else:
                    AssertionError("Method Not allowed in API")

                self.assertEqual(response.status_code, data.status_code)
