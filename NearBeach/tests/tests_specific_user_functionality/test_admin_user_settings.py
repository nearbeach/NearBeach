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


class AdminUserSettingTests(TestCase):
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
        The following test will send some kanban settings to be saved
        """
        URLTest = namedtuple(
            "URLTest",
            ["url", "args", "data", "status_code", "method"],
            defaults=["", [], {}, 200, "GET"],
        )

        data_list = [
            URLTest("user_settings_update", [], {
                "setting_type": "KANBAN_BOARD",
                "setting_data": '{"canDragCards":true,"levels":[{"level_id":1,"is_collapsed":false},{"level_id":2,"is_collapsed":true}]}'
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