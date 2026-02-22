from collections import namedtuple

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory


class BaseApiClass(APITestCase):
    """Abstracted Base Api class for testing"""
    fixtures = ["NearBeach_basic_setup.json"]
    username = ""
    password = ""
    URLTest = namedtuple(
        "URLTest",
        ["url", "data", "status_code", "method"],
        defaults=["", {}, 200, "GET"],
    )

    def setUp(self):
        """Method run on test start up - sets up the test by logging in and providing the client and factory"""
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self._login_user()
    
    def _login_user(self):
        """Private Method for logging user in"""
        response = self.client.post(
            "/api/v1/authentication/",
            {
                "username": self.username,
                "password": self.password,
                "otp_token": ""
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def _run_test_array(self, data_list):
        """Private method to run all the tests"""
        for data in data_list:
            with self.subTest(data):
                if data.method == "GET":
                    response = self.client.get(
                        data.url,
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
