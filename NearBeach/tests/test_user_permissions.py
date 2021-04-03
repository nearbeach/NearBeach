from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


class AdminUserPermissionTest(TestCase):
    """
    The admin user will have full access to the whole site - even if they are not associated with
    a group that is associated with the object.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)


        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a project with overlapping groups")

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['2']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a project without overlapping groups")


class TeamLeaderPermissionTest(TestCase):
    """
    The team leader will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_leader',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Leader can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Lead can NOT access a project without overlapping groups")


class TeamMemberPermissionTest(TestCase):
    """
    The team MEMBER will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_member',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Member can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Member can NOT access a project without overlapping groups")


class TeamInternPermissionTest(TestCase):
    """
    The team leader will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_intern',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Intern can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Intern can NOT access a project without overlapping groups")


class ReadOnlyPermissionTest(TestCase):
    """
    The read only user should be forwarded to the read only template, if they have access to at least
    one group that the object has been assigned to.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'read_only',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Read only can access a project with overlapping groups")

        # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Read Only can NOT access a project without overlapping groups")
