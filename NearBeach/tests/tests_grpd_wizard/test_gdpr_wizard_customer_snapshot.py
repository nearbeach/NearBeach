from django.test import TestCase, Client
from django.urls import reverse
from NearBeach.models import Project, Requirement, RequirementItem, Task

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
2. Admin user delete a customer using the GDPR Wizard
3. System looks for customer name within any object assigned to the organisation and strips it out
4. System deletes customer

Tests
~~~~~
We have the following objects are assigned to the organisation and has the customer details. These will be updated;
- customer -> 32
- requirement -> 1
- requirement item -> 55
- project -> 37
- task -> 99 

We have the following objects that are NOT assigned to the organistion, and will not update
- requirement -> 5
- requirement item -> 254
- project -> 3
- task -> 6

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

    def check_baseline(self):
        # Snapshot data
        name = "Dr. Andrea Bishop Desiree Ward julie72@example.org"
        requirement_1 = Requirement.objects.get(pk=1)
        requirement_5 = Requirement.objects.get(pk=5)
        requirement_item_55 = RequirementItem.objects.get(pk=55)
        requirement_item_254 = RequirementItem.objects.get(pk=254)
        project_3 = Project.objects.get(pk=3)
        project_37 = Project.objects.get(pk=37)
        task_6 = Task.objects.get(pk=6)
        task_99 = Task.objects.get(pk=99)

        # Check all data contain the information
        self.assertEqual(requirement_1.requirement_title, name)
        self.assertTrue(name in requirement_1.requirement_scope)

        self.assertEqual(requirement_5.requirement_title, name)
        self.assertTrue(name in requirement_5.requirement_scope)

        self.assertEqual(requirement_item_55.requirement_item_title, name)
        self.assertTrue(name in requirement_item_55.requirement_item_scope)

        self.assertEqual(requirement_item_254.requirement_item_title, name)
        self.assertTrue(name in requirement_item_254.requirement_item_scope)

        self.assertEqual(project_3.project_name, name)
        self.assertTrue(name in project_3.project_description)

        self.assertEqual(project_37.project_name, name)
        self.assertTrue(name in project_37.project_description)

        self.assertEqual(task_6.task_short_description, name)
        self.assertTrue(name in task_6.task_long_description)

        self.assertEqual(task_99.task_short_description, name)
        self.assertTrue(name in task_99.task_long_description)

    def check_after_run_gdpr(self):
        # Snapshot data
        name = "Dr. Andrea Bishop Desiree Ward julie72@example.org"
        requirement_1 = Requirement.objects.get(pk=1)
        requirement_5 = Requirement.objects.get(pk=5)
        requirement_item_55 = RequirementItem.objects.get(pk=55)
        requirement_item_254 = RequirementItem.objects.get(pk=254)
        project_3 = Project.objects.get(pk=3)
        project_37 = Project.objects.get(pk=37)
        task_6 = Task.objects.get(pk=6)
        task_99 = Task.objects.get(pk=99)

        # Check all data contain the information
        self.assertNotEqual(requirement_1.requirement_title, name)
        self.assertFalse(name in requirement_1.requirement_scope)

        self.assertEqual(requirement_5.requirement_title, name)
        self.assertTrue(name in requirement_5.requirement_scope)

        self.assertNotEqual(requirement_item_55.requirement_item_title, name)
        self.assertFalse(name in requirement_item_55.requirement_item_scope)

        self.assertEqual(requirement_item_254.requirement_item_title, name)
        self.assertTrue(name in requirement_item_254.requirement_item_scope)

        self.assertEqual(project_3.project_name, name)
        self.assertTrue(name in project_3.project_description)

        self.assertNotEqual(project_37.project_name, name)
        self.assertFalse(name in project_37.project_description)

        self.assertEqual(task_6.task_short_description, name)
        self.assertTrue(name in task_6.task_long_description)

        self.assertNotEqual(task_99.task_short_description, name)
        self.assertFalse(name in task_99.task_long_description)

    def test_gdpr_wizard_user_snapshot_test(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Check baseline
        self.check_baseline()

        # Run the GDPR wizard
        response = self.client.post(
            reverse(
                "gdpr_submit",
                args={}
            ),
            {
                "gdpr_object_id": 32,
                "gdpr_object_type": "customer",
                "requirement": [1],
                "requirement_item": [55],
                "project": [37],
                "task": [99],
            },
            follow=True
        )
        
        # Assert response is true
        self.assertTrue(response.status_code == 200)

        # Check to make sure all the data has been updated correctly
        self.check_after_run_gdpr()
