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


class TaskViewTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {"username": username, "password": password}

        # Setup the client
        self.client = Client()

        login_user(self.client, self)

    def test_new_task_as_team_leader(self):
        # Form Data
        form_data = {
            "task_short_description": "A simple task",
            "task_long_description": "A simple task description",
            "task_start_date": "2023-08-10T23:00:00.000Z",
            "task_end_date": "2023-08-10T23:00:00.000Z",
            "organisation": 1,
            "group_list": [1, 2]
        }

        # Use POST to submit the new task
        response = self.client.post(
            reverse("new_task_save", args={}),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_new_task_with_bad_form(self):
        # Form Data
        form_data = {
            "task_short_description": "A simple task",
            "task_long_description": "A simple task description",
            "task_start_date": "",
            "task_end_date": "2023-08-10T23:00:00.000Z",
            "organisation": 1,
            "group_list": [1, 2]
        }

        # Use POST to submit the new task
        response = self.client.post(
            reverse("new_task_save", args={}),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)


    def test_save_task_as_team_leader(self):
        # Form Data
        form_data = {
            "task_short_description": "A simple task",
            "task_long_description": "A simple task description",
            "task_start_date": "2023-08-10T23:00:00.000Z",
            "task_end_date": "2023-08-10T23:00:00.000Z",
            "task_status": "1",
        }

        # Use POST to submit the new task
        response = self.client.post(
            reverse(
                "task_information_save",
                args=[2]
            ),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_save_task_with_bad_form(self):
        # Form Data
        form_data = {
            "task_short_description": "A simple task",
            "task_long_description": "A simple task description",
            "task_start_date": "",
            "task_end_date": "2023-08-10T23:00:00.000Z",
            "task_status": "New",
        }

        # Use POST to submit the new task
        response = self.client.post(
            reverse(
                "task_information_save",
                args=[2]
            ),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
