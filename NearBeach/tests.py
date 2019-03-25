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
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/add_campus_to_customer/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/admin_group/0/permission_set/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/admin_permission_set/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/admin_add_user/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/alerts/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assign_customer_project_task/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_group_add/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_group_delete/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_group_list/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_opportunity_connection_add/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_rfc_connection_delete/0/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_rfc_connection_add/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_opportunity_connection_delete/0/0/organisation")
        self.assertRedirects(
            response,
            "/assigned_opportunity_connection_delete/0/0/organisation/", #It will then redirect to login
            status_code=301,
            target_status_code=302,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_user_add/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_user_delete/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/assigned_user_list/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/associate/0/0/P")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/associated_projects/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/associated_task/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_add/0/project/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_client_delete/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_client_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_client_list/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_list/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_list/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/bug_search/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/campus_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/campus_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/change_task_list/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_change_task/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/cost_information/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/customer_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/customer_campus_information/0/CUST/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/customer_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/active_projects/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/active_quotes/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/active_requirements/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/active_tasks/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/group_active_projects/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/group_active_tasks/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/group_opportunities/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/dashboard/opportunities/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/deactivate_campus/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_campus_contact/0/CUST/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_cost/0/0/P")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_group/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_document/0f6b2aa9-deaf-43f0-8064-aba7deb9571a/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_folder/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_permission_set/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/delete_tag/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/diagnostic_information/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/diagnostic_test_database/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/diagnostic_test_document_upload/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/diagnostic_test_email/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/diagnostic_test_location_services/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/diagnostic_test_recaptcha/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/email_history/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/email_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/email/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/extract_quote/0f6b2aa9-deaf-43f0-8064-aba7deb9571a/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/extract_requirement/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/group_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_customer_contact_history/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_organisation_contact_history/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_project_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_project_history/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_task_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/information_task_history/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_edit_card/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_edit_xy_name/0/column/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_list/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/kanban_properties/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_read_only/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_requirement_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/kanban_requirement_item_update/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/list_of_tags/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/list_of_taxes_deactivate/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/list_of_taxes_edit/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/list_of_taxes_information/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/list_of_taxes_list/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/list_of_taxes_new/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/logout/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/lookup_product/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/merge_tags/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/merge_tags/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/my_profile/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_bug_client/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_campus/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_group/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_kanban_board/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_kanban_requirement_board/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_kudos/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_opportunity/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_permission_set/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_project/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_quote_template/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_quote/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_request_for_change/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_requirement/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_requirement_item/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_task/0/organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_task/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/new_user/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/opportunity_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/organisation_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/organisation_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/permission_denied/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/permission_set_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/preview_requirement/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/product_and_service_discontinued/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/product_and_service_edit/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/product_and_service_new/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/product_and_service_search/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/project_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/project_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/project_remove_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_delete_line_item/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_delete_responsible_customer/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_list_of_line_items/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_new_line_item/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_responsible_customer/0/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_responsible_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/quote_template_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/rename_document/0f6b2aa9-deaf-43f0-8064-aba7deb9571a/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/request_for_change_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/requirement_documents_uploads/0/requirement/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/requirement_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/requirement_item_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/requirement_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/resolve_project/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/resolve_task/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_customer/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_group/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_organisation/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_permission_set/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_projects_task/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_tags/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_templates/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search_users/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/search/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/tag_information/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/task_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/task_readonly/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/task_remove_customer/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/timeline_data/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/timeline/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/to_do_complete/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/to_do/0/project/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/user_information/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/user_permissions/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/user_want_remove/0/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        c = Client()
        response = c.get("/user_want_view/")
        self.assertRedirects(
            response,
            "/login",
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )


        c = Client()
        response = c.get("/user_weblink_view/")
        self.assertRedirects(
            response,
            "/login",
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



        #Now test dashboard directly
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 301)

        
