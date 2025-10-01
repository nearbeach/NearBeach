from django.apps import apps
from django.test import TestCase, Client
from django.urls import reverse

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
We'll loop through ever single table, and grab a count of rows from those tables and compare it afterwards.

The baseline count will make sure we'll exclude any user fields that contains the delete user (as the cascade effect
will remove these values). The "creation_user" and "change_user" fields should update automatically to the admin user (
this is tested throughly in another test case).

We can loop through each table to create the counts.
"""


class GdprWizardCustomerCount(TestCase):
    fixtures = ['NearBeach_gdpr_setup.json']
    data_dict = {}

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

    def after_update_checking(self):
        nearbeach_tables = apps.get_app_config("NearBeach").get_models()
        for single_table in nearbeach_tables:
            results = single_table.objects.all()

            with self.subTest(F"GDPR wizard customer count: {single_table.__name__}"):
                self.assertEqual(
                    len(results),
                    self.data_dict[single_table.__name__],
                )

    def setup_baseline_count(self):
        nearbeach_tables = apps.get_app_config("NearBeach").get_models()
        for single_table in nearbeach_tables:
            condition_1 = hasattr(single_table, "customer_id")

            results = single_table.objects.filter()

            if condition_1:
                results = results.exclude(
                    customer_id=23,
                )

            self.data_dict[single_table.__name__] = results.count()

    def test_gdpr_wizard_customer_count_test(self):
        c = Client()

        # User will be logged in
        login_user(c, self)
        
        # Setup the baseline
        self.setup_baseline_count()
        
        # Run the GDPR wizard
        response = self.client.post(
            reverse(
                "gdpr_submit",
                args={}
            ),
            {
                "gdpr_object_id": 23,
                "gdpr_object_type": "customer",
            },
            follow=True
        )

        self.assertTrue(response.status_code, 200)

        # Check the results
        self.after_update_checking()
