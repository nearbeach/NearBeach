from django.test import TestCase, Client
from NearBeach.models import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
# Create your tests here.

import datetime


class ModelsTestCase(TestCase):
    def setUp(self):
        """
        Setup users for login purposes
        """
        # Create users
        admin_user = User(
            username='admin',
            first_name='Admin',
            last_name='User',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )
        admin_user.set_password("test")
        admin_user.save()

        basic_user = User(
            username='basic_user',
            first_name='Basic',
            last_name='User',
            is_superuser=False,
            is_active=True,
            is_staff=True,
        )
        basic_user.set_password("basic_user")
        basic_user.save()

        read_only_user = User(
            username='read_only_user',
            first_name='Read Only',
            last_name='User',
            is_superuser=False,
            is_active=True,
            is_staff=True,
        )
        read_only_user.set_password("read_only_user")
        read_only_user.save()

        # Setup permission sets
        admin_access = permission_set.objects.create(
            permission_set_name="Admin Access",
            administration_assign_user_to_group=4,
            administration_create_group=4,
            administration_create_permission_set=4,
            administration_create_user=4,
            bug_client=4,
            customer=4,
            kanban=4,
            kanban_card=4,
            organisation=4,
            project=4,
            requirement=4,
            task=4,
            document=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
            change_user=admin_user,
        )

        basic_user_access = permission_set.objects.create(
            permission_set_name="Basic User Access",
            administration_assign_user_to_group=0,
            administration_create_group=0,
            administration_create_permission_set=0,
            administration_create_user=0,
            bug_client=3,
            customer=3,
            kanban=3,
            kanban_card=3,
            organisation=3,
            project=3,
            requirement=3,
            task=3,
            document=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
            change_user=admin_user,
        )

        read_only_access = permission_set.objects.create(
            permission_set_name="Read Only Access",
            administration_assign_user_to_group=0,
            administration_create_group=0,
            administration_create_permission_set=0,
            administration_create_user=0,
            bug_client=1,
            customer=1,
            kanban=1,
            kanban_card=1,
            organisation=1,
            project=1,
            requirement=1,
            task=1,
            document=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
            change_user=admin_user,
        )

        # Create admin group
        administration_group = group.objects.create(
            group_name="Administration",
            change_user=admin_user,
        )

        user_acceptance_testing_group = group.objects.create(
            group_name="User Acceptance Testing",
            change_user=admin_user,
        )

        no_group = group.objects.create(
            group_name="No Group",
            change_user=admin_user,
        )

        # Add users to groups
        add_admin_to_group_1 = user_group.objects.create(
            username=admin_user,
            group=administration_group,
            permission_set=admin_access,
            change_user=admin_user,
        )

        add_admin_to_group_2 = user_group.objects.create(
            username=admin_user,
            group=user_acceptance_testing_group,
            permission_set=admin_access,
            change_user=admin_user,
        )

        add_basic_to_group_1 = user_group.objects.create(
            username=basic_user,
            group=user_acceptance_testing_group,
            permission_set=basic_user_access,
            change_user=admin_user,
        )

        add_read_only_to_group_1 = user_group.objects.create(
            username=read_only_user,
            group=user_acceptance_testing_group,
            permission_set=read_only_access,
            change_user=admin_user,
        )

        print("Creation of the database successful")

    def test_login_page(self):
        """
        Before completing any other tests. We need to make sure that the login page is working fine.
        This is a critical piece.
        :return: if it worked or not
        """
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)
        print("Login Page working correctly")


class NonLoggedInRedirectionTestCases(TestCase):
    """
    The following test cases will look at those users who have not logged in. They will force the user back to the
    login page.
    """
    def test_login_page(self):
        """
        Before completing any other tests. We need to make sure that the login page is working fine.
        This is a critical piece.
        :return: if it worked or not
        """
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)

    def dashboard_redirect(self):
        """
        Make sure a user who has not logged in gets redirected to login screen
        :return:
        """
        c = Client()

        # DASHBOARD
        response = c.get("/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        print("Non logged in user redirect from <dashboard> to <login> screen")

    def new_requirement_redirect(self):
        c = Client()
        response = c.get("/new_requirement")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        print("Non logged in user redirect from <new_requirement> to <login> screen")




class LoggedInTestCases(TestCase):
    def test_login_page(self):
        """
        Before completing any other tests. We need to make sure that the login page is working fine.
        This is a critical piece.
        :return: if it worked or not
        """
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)

    def log_admin_user_in(self):
        """
        A logged in administration user will be directed to the dashboard page "/"
        :return:
        """
        admin_user = User.objects.get(username='admin')

        response = self.client.post(
            reverse('login'),
            {
                'username': 'test',
                'password': 'test',
            }
        )

        print("Administration User Successfully Logged in")

    def dashboard(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

        print("Administration User successfully loaded <dashbaord>")

    def new_requirement(self):
        c = Client()
        response = c.get("/new_requirement")
        self.assertEqual(response.status_code, 200)

        print("Administration User successfully loaded <new_requirement>")


    def logout_administrator(self):
        c = Client()
        response = c.get("/logout")

        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        print("Administrator successfully logged out.")

