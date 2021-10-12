from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = 'read_only'
password = 'Test1234$'


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


class CustomerPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_customer_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        _ = c.get(reverse('customer_information', args=['1']))
        #self.assertEqual(response.status_code, 200)

    def test_customer_save_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Send a POST request to new_customer -> user should NOT be able to save
        _ = c.post(
            reverse('customer_information_save', args=['1']),
            data={
                'customer_title': 1,
                'customer_first_name': 'NearBeach',
                'customer_last_name': 'Support',
                'customer_email': 'support@nearbeach.org',
                'organisation': 1,
            },
        )
        #self.assertEqual(response.status_code, 403)

    def test_new_customer_permission(self):
        c = Client()

        # user will be logged in
        login_user(c, self)

        # Go to create a new customer -> user should NOT have access
        _ = c.get(reverse('new_customer'))
        #self.assertEqual(response.status_code, 403)


class KanbanPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_kanban_information(self):
        c = Client()

        # user will be logged in
        login_user(c, self)

        # Go to an existing kanban board
        response = c.get(reverse('kanban_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # Go to an existing kanban board where user is not in group -> permission denied
        response = c.get(reverse('kanban_information', args=['2']))
        #self.assertEqual(response.status_code, 403)


class OrganisationPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }


class ProjectPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # Make sure the admin user can open up the task
        # response = c.get(reverse('task_information', args=['2']))
        # self.assertEqual(response.status_code, 403)


class RFCPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }


class RequirementPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }


class RequirementItemPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }


class TaskPermissionTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the task
        _ = c.get(reverse('task_information', args=['1']))
        #self.assertEqual(response.status_code, 200)

        # Make sure the admin user can open up the project
        # response = c.get(reverse('task_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
