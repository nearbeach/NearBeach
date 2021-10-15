from django.contrib.auth.models import User
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
        response = c.get(reverse('customer_information', args=['1']))
        self.assertEqual(response.status_code, 200)

    def test_customer_save_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Send a POST request to new_customer -> user should NOT be able to save
        response = c.post(
            reverse('customer_information_save', args=['1']),
            data={
                'customer_title': 1,
                'customer_first_name': 'NearBeach',
                'customer_last_name': 'Support',
                'customer_email': 'support@nearbeach.org',
                'organisation': 1,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_new_customer_permission(self):
        c = Client()

        # user will be logged in
        login_user(c, self)

        # Go to create a new customer -> user should NOT have access
        response = c.get(reverse('new_customer'))
        self.assertEqual(response.status_code, 200)


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
        self.assertEqual(response.status_code, 200)


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
        response = c.get(reverse('task_information', args=['2']))
        self.assertEqual(response.status_code, 200)


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
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['2']))
        self.assertEqual(response.status_code, 200)


class AdministrationTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_search_users(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can go to the /search/users panel
        response = c.get(reverse('search_user'))
        self.assertEqual(response.status_code, 200)

        # Send data to the backend
        response = c.post(
            reverse('search_user'),
            {'search': 'project'}
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_user_information(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can go to the user/1
        response = c.get(reverse('user_information', args=[2]))
        self.assertEqual(response.status_code, 200)

        # Make sure the admin user can save information
        response = c.post(
            reverse('user_information_save', args=[2]),
            {
                'first_name': 'Team',
                'last_name': 'Leader',
                'email': 'support@nearbeach.org',
                'is_active': True,
                'is_superuser': False,
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_bad_user_information_forms(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can go to the user/1
        _ = c.get(reverse('user_information', args=[2]))

        # The following tests will make sure the user can't submit bad forms
        # Blank First name
        #response = c.post(
        #    reverse('user_information_save', args=[2]),
        #    {
        #        'first_name': '',
        #        'last_name': 'Name',
        #        'email': 'support@nearbeach.org',
        #        'is_active': True,
        #        'is_superuser': False,
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

        # Blank Lastname
        #response = c.post(
        #    reverse('user_information_save', args=[2]),
        #    {
        #        'first_name': 'First',
        #        'last_name': '',
        #        'email': 'support@nearbeach.org',
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

        # Blank Email
        #response = c.post(
        #    reverse('user_information_save', args=[2]),
        #    {
        #        'first_name': 'First',
        #        'last_name': 'Name',
        #        'email': '',
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

        # Blank Passwords
        #response = c.post(
        #    reverse('user_information_save', args=[2]),
        #    {
        #        'first_name': 'First',
        #        'last_name': 'Name',
        #        'email': 'support@nearbeach.org',
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

        # Blank Firstname
        #response = c.post(
        #    reverse('user_information_save', args=[2]),
        #    {
        #        'first_name': 'First',
        #        'last_name': 'Name',
        #        'email': 'support@nearbeach.org',
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

    def test_admin_new_user(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can go to the new_user
        response = c.get(reverse('new_user'))
        self.assertEqual(response.status_code, 200)

        # Make sure the admin user can submit a new user
        response = c.post(
            reverse('new_user_save'),
            {
                'username': 'random_user',
                'first_name': 'First',
                'last_name': 'Name',
                'email': 'support@nearbeach.org',
                'password1': 'Test1234$',
                'password2': 'Test1234$'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_bad_new_user_forms(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can go to the user/1
        response = c.get(reverse('user_information', args=[2]))
        # The following tests will make sure the user can't submit bad forms
        # Blank Username
        response = c.post(
            reverse('new_user_save'),
            {
                'username': '',
                'first_name': 'First',
                'last_name': 'Name',
                'email': 'support@nearbeach.org',
                'password1': 'Test1234$',
                'password2': 'Test1234$'
            }
        )
        self.assertEqual(response.status_code, 400)

        # Blank Email
        #response = c.post(
        #    reverse('new_user_save'),
        #    {
        #        'username': 'form_fail',
        #        'first_name': 'First',
        #        'last_name': 'Name',
        #        'email': '',
        #        'password1': 'Test1234$',
        #        'password2': 'Test1234$'
        #    }
        #)
        #self.assertEqual(response.status_code, 400)

        # Blank Passwords
        # response = c.post(
        #     reverse('new_user_save'),
        #     {
        #         'username': 'form_fail',
        #         'first_name': 'First',
        #         'last_name': 'Name',
        #         'email': 'support@nearbeach.org',
        #         'password1': '',
        #         'password2': 'Test1234$'
        #     }
        # )
        # self.assertEqual(response.status_code, 400)

        # # Blank Firstname
        # response = c.post(
        #     reverse('new_user_save'),
        #     {
        #         'username': 'form_fail',
        #         'first_name': 'First',
        #         'last_name': 'Name',
        #         'email': 'support@nearbeach.org',
        #         'password1': 'Test1234$',
        #         'password2': ''
        #     }
        # )
        # self.assertEqual(response.status_code, 400)



