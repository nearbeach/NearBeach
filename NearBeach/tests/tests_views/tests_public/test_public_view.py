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


class PublicViewTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {"username": username, "password": password}

        # Setup the client
        self.client = Client()

        login_user(self.client, self)

    def test_create_public_link_fail(self):
        """
        We are creating a public link against an object we do not have access too
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("create_public_link", args=["project", 1]))
        self.assertEqual(response.status_code, 403)

    def test_create_public_links_list_fail(self):
        """
        We are creating a public link against an object we do not have access too
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("get_public_links", args=["project", 1]))
        self.assertEqual(response.status_code, 403)

    def test_update_public_link_list_fail(self):
        """
        We are creating a public link against an object we do not have access too
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(
            reverse("update_public_link", args=["project", 1]),
            data={"public_link_id": "3d7346c4-05b6-41df-816a-eff814d9bbd0", "public_link_is_active": "False"}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_public_link_fail(self):
            """
            We are creating a public link against an object we do not have access too
            """
            c = Client()

            # User wil be logged in
            login_user(c, self)

            # Get data of wrong location - gets a 403
            response = c.post(
                reverse("delete_public_link", args=["project", 1]),
                data={"public_link_id": "3d7346c4-05b6-41df-816a-eff814d9bbd0"}
            )
            self.assertEqual(response.status_code, 403)

    def test_create_public_link_pass(self):
        """
        We are creating a public link against an object we have access too.
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("create_public_link", args=["project", 2]))
        self.assertEqual(response.status_code, 200)

    def test_create_public_links_list_success(self):
        """
        We are creating a public link against an object we do not have access too
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("get_public_links", args=["project", 2]))
        self.assertEqual(response.status_code, 200)

    def test_delete_public_link_success(self):
            """
            We are creating a public link against an object we do not have access too
            """
            c = Client()

            # User wil be logged in
            login_user(c, self)

            # Get data of wrong location - gets a 403
            response = c.post(
                reverse("delete_public_link", args=["project", 2]),
                data={"public_link_id": "5f369dc9-a0bb-416d-9779-92576d0500bb"}
            )
            self.assertEqual(response.status_code, 200)

    def test_update_public_links_list_success(self):
        """
        We are creating a public link against an object we do not have access too
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        response = c.post(
            reverse("update_public_link", args=["project", 2]),
            data={"public_link_id": "5f369dc9-a0bb-416d-9779-92576d0500bb", "public_link_is_active": "False"}
        )
        self.assertEqual(response.status_code, 200)