from django.test import TestCase, Client
from django.urls import reverse
from NearBeach.models import Project

# Declaration of Username and Password
username = 'admin'
password = 'Test1234$'

def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


"""
Method
~~~~~~
1. Admin user goes to the GDPR wizard
2. Admin user delete a USER using GDPR wizard
3. System updates all "creation_user" and "change_user" fields that are assigned to the deleted user, and updates them
   to be the current logged in users id
4. System deletes the user from the user table

Tests
~~~~~
As the update occurs in a for loop that extends ALL tables within the system, we'll only test one table. If it 
successfully occurs in that one table, it is assumed it will successfully occur in the other tables.

We'll focus on the project table, find two lists;
- Projects created by the deleted user
- Projects updated by the deleted user

We'll run the GDPR wizard against the delete user.

Check all projects in both lists;
1. Still exist
2. And the fields have been updated to the admin user
"""
class GdprWizardSnapshotTest(TestCase):
    fixtures = ['NearBeach_gdpr_setup.json']

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

    def test_gdpr_wizard_user_snapshot_test(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Snapshot data
        project_creation_user = Project.objects.filter(creation_user=6)
        project_change_user = Project.objects.filter(change_user=6)

        # Run the GDPR wizard
        response = self.client.post(
            reverse(
                "gdpr_submit",
                args={}
            ),
            {
                "gdpr_object_id": 6,
                "gdpr_object_type": "user",
            },
            follow=True
        )

        # Assert response is true
        self.assertTrue(response.status_code == 200)

        # Check to make sure all the data has been updated correctly
        after_update_creation_user = Project.objects.filter(
            creation_user=1,
            project_id__in=project_creation_user.values("project_id"),
        )
        after_update_change_user = Project.objects.filter(
            change_user=1,
            project_id__in=project_change_user.values("project_id"),
        )

        # Assert that both sets contain the same elements
        self.assertEqual(after_update_creation_user.count(), project_creation_user.count())
        self.assertEqual(after_update_change_user.count(), project_change_user.count())
