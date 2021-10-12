from django.contrib.auth.models import User
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.db.models import Q, Max

import unittest
import json
from NearBeach.models import user_group, group, object_assignment

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

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['2']))
        self.assertEqual(response.status_code, 200)

        c.get(reverse('logout'))

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

        c.get(reverse('logout'))

    def test_kanban_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[1]))
        self.assertEqual(response.status_code, 200)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[2]))
        self.assertEqual(response.status_code, 200)

    def test_new_organisation_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('new_organisation'))
        self.assertEqual(response.status_code, 200)

    def test_organisation_information_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('organisation_information', args=[1]))
        self.assertEqual(response.status_code, 200)


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

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('task_information', args=['2']))
        # self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

    def test_kanban_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[1]))
        self.assertEqual(response.status_code, 200)

        # TEMP CODE - CHECK USER PERMISSIONS LOGIC
        user_group_results = user_group.objects.filter(
            is_deleted=False,
            username=2,
        )

        group_results = group.objects.filter(
            Q(
                is_deleted=False,
                # The object_lookup groups
                group_id__in=object_assignment.objects.filter(
                    is_deleted=False,
                    kanban_board_id=2,
                ).values('group_id'),
            ) &
            Q(
                group_id__in=user_group_results.values('group_id')
            )
        )

        print("Group Results Length: %s" % len(group_results))

        # Make sure the admin user can open the kanban
        response_2 = c.get(reverse('kanban_information', args=[2]))
        self.assertEqual(response_2.status_code, 403)

    def test_new_organisation_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('new_organisation'))
        self.assertEqual(response.status_code, 200)

    def test_organisation_information_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('organisation_information', args=[1]))
        self.assertEqual(response.status_code, 200)


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

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # # Make sure the admin user can open up the task
        #response = c.get(reverse('task_information', args=['2']))
        #self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

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

    def test_project_permissions_ti(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # # Make sure the admin user can open up the project
        #response = c.get(reverse('project_information', args=['2']))
        #self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)

        # # Make sure the admin user can open up the task
        #response = c.get(reverse('task_information', args=['2']))
        #self.assertEqual(response.status_code, 403)

        c.get(reverse('logout'))

