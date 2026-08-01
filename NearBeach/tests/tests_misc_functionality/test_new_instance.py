from NearBeach.models import Group, PermissionSet, UserGroup
from django.test import TestCase, Client


class NewInstanceTests(TestCase):
    """Test for new instance"""
    fixtures = ["NearBeach_no_setup.json"]
    username = "admin"
    password = "Test1234$"

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
                "username": "admin",
                "password": "Test1234$",
                "otp_token": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # Check the final data
        permission_set = PermissionSet.objects.all()
        group = Group.objects.all()
        user_group = UserGroup.objects.all()

        # Assert they are all empty
        self.assertTrue(len(permission_set) > 0)
        self.assertTrue(len(group) > 0)
        self.assertTrue(len(user_group) > 0)
