from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "team_leader"
password = "Test1234$"
long_string = """
    There once was a cat called Socks, she liked to eat treats whilst on stream. People liked to feed her treats because
    she was adoriable. Currently she is licking my arm, I think because she enjoyed the treats she got on stream. Socks
    does like to every now and then meow into the microphone.
"""


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class TestNote(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        self.credentials = {"username": username, "password": password}

    def test_note_delete_fail(self):
        """
        The following test will try and delete a note they don't have access too. It should fail
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("delete_note", args=["2"]))
        self.assertEqual(response.status_code, 403)

    def test_note_update_fail(self):
        """
        The following test will try and delete a note they don't have access too. It should fail
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(
            reverse("update_note", args=["2"]),
            data={'object_note_id': 2, 'object_note': 'Hello World'}
        )
        self.assertEqual(response.status_code, 403)

    def test_note_delete_success(self):
        """
        The following test will try and delete a note they have access too. It should pass
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("delete_note", args=["3"]))
        self.assertEqual(response.status_code, 200)

    def test_note_update_success(self):
        """
        The following test will try and delete a note they have access too. It should pass
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(
            reverse("update_note", args=["3"]),
            data={'object_note_id': 3, 'object_note': 'Hello World'}
        )
        self.assertEqual(response.status_code, 200)
