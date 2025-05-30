from django.test import TestCase, Client
from django.urls import reverse


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class TestPermissionDenied(TestCase):
    """
    The admin user will have full access to the whole site - even if they are not associated with
    a group that is associated with the object.
    """

    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        self.credentials = {
            "two_factor_login_view-current_step": "auth",
            "auth-username": "admin",
            "auth-password": "Test1234$"
        }

    def test_permission_denied(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse("test_permission_denied"))
        self.assertEqual(response.status_code, 403)

        c.get(reverse("logout"))
