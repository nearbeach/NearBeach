from django.test import TestCase, Client
from .models import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
# Create your tests here.

class ModelsTestCase(TestCase):
    def setUp(self):
        user1 = User(
            username='test',
            first_name='Test',
            last_name='User',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )
        user1.set_password("test")
        user1.save()

        #Setup the organisation
        org1 = organisation.objects.create(
            organisation_name="NearBeach",
            organisation_website="https://nearbeach.org",
            organisation_email="support@nearbeach.org",
            change_user=user1,
        )


        #Setup permissions
        submit_permission_set = permission_set.objects.create(
            permission_set_name="Administration Permission Set",
            administration_assign_user_to_group=4,
            administration_create_group=4,
            administration_create_permission_set=4,
            administration_create_user=4,
            assign_campus_to_customer=4,
            associate_project_and_task=4,
            bug=4,
            bug_client=4,
            customer=4,
            email=4,
            invoice=4,
            invoice_product=4,
            kanban=4,
            kanban_card=4,
            opportunity=4,
            organisation=4,
            organisation_campus=4,
            project=4,
            quote=4,
            requirement=4,
            requirement_link=4,
            task=4,
            tax=4,
            template=4,
            document=1,
            contact_history=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
            change_user=user1,
        )

        # Create admin group
        submit_group = group.objects.create(
            group_name="Administration",
            change_user=user1,
        )

        # Add user to admin group
        submit_user_group = user_group.objects.create(
            username=user1,
            group=group.objects.get(group_id=1),
            permission_set=permission_set.objects.get(permission_set_id=1),
            change_user=user1,
        )

    def test_organisation(self):
        org1 = organisation.objects.get(organisation_id=1)
        self.assertEqual(org1.organisation_name,"NearBeach")

    def test_login_page(self):
        """
        Before completing any other tests. We need to make sure that the login page is working fine.
        This is a critical piece.
        :return: if it worked or not
        """
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login_page(self):
        """
        We have not logged the user in yet. This will check to see if the user will be redirected
        to the login page from certain pages.
        :return:
        """
        c = Client()
        response = c.get("/")
        self.assertRedirects(
            response,
            "/login?next=/",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

    def test_login_page(self):
        """
        We will login as the admin. From here we will continue to go to several pages.

        NOTE - I will need to apply the permission sets to the user
        :return:
        """
        print("Logging in user through POST")
        user1 = User.objects.get(username='test')
        print("Password: " + str(user1.password))

        response = self.client.post(
            reverse('login'),
            {
                'username': 'test',
                'password': 'test',
            }
        )
        self.assertRedirects(
            response,
            "/alerts/",
            status_code=302,
            target_status_code=302, #Lands on alerts page, but gets redirected again.
            msg_prefix='',
            fetch_redirect_response=True
        )

        #Now test to see if you stay on the dashboard page
        response = self.client.get('/') #Will be redirected to alerts then dashboard
        self.assertRedirects(
            response,
            "/dashboard/",
            status_code=302,
            target_status_code=200,  # Lands on alerts page, but gets redirected again.
            msg_prefix='',
            fetch_redirect_response=True
        )

        #Now test dashboard directly
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 301)
