from NearBeach.models import Group, PermissionSet, UserGroup
from django.test import TestCase, Client
from unittest.mock import patch


class NewInstanceNonAdminTests(TestCase):
    """Test for new instance"""
    fixtures = ["NearBeach_no_setup.json"]

    def setUp(self):
        # Disable throttling for the auth endpoint during tests
        patcher = patch(
            "NearBeach.views.api_v1.authentication.authentication_api_view.AuthenticationView.throttle_classes",
            [],
        )
        patcher.start()

    def test_new_instance_setup_correctly(self):
        """
        Test - new instance is setup correctly on first login

        Method to replicate
        ~~~~~~~~~~~~~~~~~~~
        1. Check permission set table is empty
        2. Check groups table is empty
        3. Check user group table is empty
        4. Login
        5. Assert permission set table is no longer empty
        6. Assert groups table is no longer empty
        7. Assert user group table is no longer empty

        Expected Results
        ~~~~~~~~~~~~~~~~
        On first login - those tables are filled with data
        """

        # Check initial data
        permission_set = PermissionSet.objects.all()
        group = Group.objects.all()
        user_group = UserGroup.objects.all()

        # Assert they are all empty
        self.assertEqual(len(permission_set), 0)
        self.assertEqual(len(group), 0)
        self.assertEqual(len(user_group), 0)

        # Login
        c = Client()
        response = c.post(
            "/api/v1/authentication/",
            {
                "username": "team_leader",
                "password": "Test1234$",
                "otp_token": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 401)

        # Check the final data
        permission_set = PermissionSet.objects.all()
        group = Group.objects.all()
        user_group = UserGroup.objects.all()

        # Assert they are all empty as an admin user did not log in
        self.assertEqual(len(permission_set), 0)
        self.assertEqual(len(group), 0)
        self.assertEqual(len(user_group), 0)
