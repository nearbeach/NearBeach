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


class ProjectViewTests(TestCase):
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

    def test_new_project_as_team_leader(self):
        # Form Data
        form_data = {
            "project_name": "A simple project",
            "project_description": "A simple project description",
            "project_start_date": "2023-08-10T23:00:00.000Z",
            "project_end_date": "2023-08-10T23:00:00.000Z",
            "organisation": 1,
            "group_list": [1, 2],
        }

        # Use POST to submit the new project
        response = self.client.post(
            reverse("new_project_save", args={}),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_new_project_with_bad_form(self):
        # Form Data - that is INCORRECT - will fail
        # IN future - do permutation of bad form data to test ALL fields
        form_data = {
            "project_name": "A simple project",
            "project_description": "A simple project description",
            "project_start_date": "",
            "project_end_date": "",
            "organisation": 1,
            "group_list": [1, 2]
        }

        # Use POST to submit the new project
        response = self.client.post(
            reverse("new_project_save", args={}),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

    def test_save_project_as_team_leader(self):
        # Form Data
        form_data = {
            "project_name": "A simple project",
            "project_description": "A simple project description",
            "project_start_date": "2023-08-10T23:00:00.000Z",
            "project_end_date": "2023-08-10T23:00:00.000Z",
            "project_status": "1",
            "project_priority": "2",
            "project_story_point": "2",
        }

        # Use POST to submit the new project
        response = self.client.post(
            reverse(
                "project_information_save",
                args=[2]
            ),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_save_project_with_bad_form_data(self):
        # Form Data
        form_data = {
            "project_name": "A simple project",
            "project_description": "A simple project description",
            "project_start_date": "",
            "project_end_date": "",
            "project_status": "New",
        }

        # Use POST to submit the new project
        response = self.client.post(
            reverse(
                "project_information_save",
                args=[2]
            ),
            form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
