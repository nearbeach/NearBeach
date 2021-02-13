from django.test import TestCase, Client
from django.urls import reverse
from .function_tests import *

"""
The following test will;
1. Not log in a user
2. Visit every single URL

Where the expected results would be;
1. Login page will load correctly
2. Every other page redirects to the login page
"""


class CheckLoginPage(TestCase):
    def test_login_page(self):
        # Make sure the login page does work
        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        print("Non logged in users can get access to the login page")


class CheckCustomerInformation(TestCase):
    def test_customer_information_page(self):
        # Make sure the customer information page redirects
        c = Client()
        response_get = c.get(reverse('customer_information', args=[1]))
        response_post = c.post(reverse('customer_information_save',args=[1]))

        # Check
        self.assertRedirects(
            response_get,
            reverse('login'),
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        self.assertRedirects(
            response_post,
            reverse('login'),
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        # Notify tester
        print("Non logged in users get redirected when visiting customers")


class CheckDashboard(TestCase):
    def test_dashboard(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        # Setup the response array
        response_array = [
            c.get(reverse('dashboard')),
            c.get(reverse('get_bug_list')),
            c.get(reverse('get_my_objects')),
        ]

        # Check the data in the array
        assertRedirectsToLogin(response_array, self)

        # Tell tester of results
        print("Non Logged in users redirected when visiting dashboard")


class CheckDocumentation(TestCase):
    def test_documentation(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        # The get components should receive a 405
        response_get_array = [
            c.get(reverse('document_add_folder', args=['project', 1])),
            c.get(reverse('document_add_link', args=['project', 1])),
            c.get(reverse('document_list_files', args=['project', 1])),
            c.get(reverse('document_list_folders', args=['project', 1])),
            c.get(reverse('document_upload', args=['project', 1])),
            c.get(reverse('document_get_max_upload')),
        ]

        # Check the array
        assertEqual405(response_get_array, self)

        # The POST components should be redirected
        response_post_array = [
            c.post(reverse('document_add_folder', args=['project', 1])),
            c.post(reverse('document_add_link', args=['project', 1])),
            c.post(reverse('document_list_files', args=['project', 1])),
            c.post(reverse('document_list_folders', args=['project', 1])),
            c.post(reverse('document_upload', args=['project', 1])),
            c.post(reverse('document_get_max_upload')),
        ]

        #Check the array
        assertRedirectsToLogin(response_post_array, self)

        print("Non Logged in users redirected when visiting documentation")


class CheckKanban(TestCase):
    def test_kanban_information(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        # Setup response array
        response_array = [
            c.get(reverse('kanban_information', args=[1])),
            c.get(reverse('add_kanban_link', args=[1, 'project'])),
            c.get(reverse('kanban_link_list', args=[1, 'project'])),
            c.get(reverse('new_kanban_card', args=[1])),
            c.get(reverse('move_kanban_card', args=[1])),
            c.get(reverse('check_kanban_board_name')),
            c.get(reverse('kanban_update_card')),
        ]

        # Check the array
        assertRedirectsToLogin(response_array, self)

        print("Non Logged in users redirected when visiting kanban information")


class CheckPrivateDocument(TestCase):
    def test_private_document(self):
        # Make sure the user gets redirected to the login page
        c = Client()
        response_get = c.get(reverse('private_download_file', args=['12345678-1234-5678-1234-567812345678']))

        self.assertRedirects(
            response_get,
            reverse('login'),
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )

        print("Non Logged in users redirected when visiting private document")


class CheckNew(TestCase):
    def new(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        response_array = [
            c.get(reverse('new_customer')),
            c.get(reverse('new_kanban')),
            c.get(reverse('new_organisation')),
            c.get(reverse('new_project')),
            c.get(reverse('new_request_for_change')),
            c.get(reverse('new_requirement')),
            c.get(reverse('new_requirement_item', args=[1])),
            c.get(reverse('new_task')),
        ]

        # Check the array
        assertEqual405(response_array, self)

        print("Non Logged in users redirected when visiting private document")

    def new_save(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        response_array = [
            c.post(reverse('new_customer_save')),
            c.post(reverse('new_kanban_save')),
            c.post(reverse('new_organisation_save')),
            c.post(reverse('new_project_save')),
            c.post(reverse('new_request_for_change_save')),
            c.post(reverse('new_requirement_save')),
            c.post(reverse('new_requirement_item_save', args=[1])),
            c.post(reverse('new_task_save')),
        ]

        # Check the array
        assertRedirectsToLogin(response_array, self)


class CheckObjects(TestCase):
    def test_objects_get(self):
        # Setup the client
        c = Client()

        # Setup the request array
        response_array = [
            c.get(reverse('add_bug', args=['project',1])),
            c.get(reverse('add_customer', args=['project',1])),
            c.get(reverse('add_group', args=['project',1])),
            c.get(reverse('add_link', args=['project',1])),
            c.get(reverse('add_notes', args=['project',1])),
            c.get(reverse('add_user', args=['project',1])),
            c.get(reverse('associated_objects', args=['project',1])),
            c.get(reverse('bug_client_list')),
            c.get(reverse('bug_list', args=['project',1])),
            c.get(reverse('customer_list', args=['project',1])),
            c.get(reverse('customer_list_all', args=['project',1])),
            c.get(reverse('group_list', args=['project',1])),
            c.get(reverse('group_list_all', args=['project',1])),
            c.get(reverse('link_list', args=['project',1,'task'])),
            c.get(reverse('note_list', args=['project',1])),
            c.get(reverse('object_link_list', args=['project',1])),
            c.get(reverse('query_bug_client', args=['project',1])),
            c.get(reverse('user_list', args=['project',1])),
            c.get(reverse('user_list_all', args=['project',1])),
            c.get(reverse('lead_user_list')),
        ]

        # Cheeck the array
        assertEqual405(response_array, self)

        print("Non Logged in users redirected when visiting objects (GET)")

    def test_objects_post(self):
        # Setup the client
        c = Client()

        # Setup the request array
        response_array = [
            c.post(reverse('add_bug', args=['project', 1])),
            c.post(reverse('add_customer', args=['project', 1])),
            c.post(reverse('add_group', args=['project', 1])),
            c.post(reverse('add_link', args=['project', 1])),
            c.post(reverse('add_notes', args=['project', 1])),
            c.post(reverse('add_user', args=['project', 1])),
            c.post(reverse('associated_objects', args=['project', 1])),
            c.post(reverse('bug_client_list')),
            c.post(reverse('bug_list', args=['project', 1])),
            c.post(reverse('customer_list', args=['project', 1])),
            c.post(reverse('customer_list_all', args=['project', 1])),
            c.post(reverse('group_list', args=['project', 1])),
            c.post(reverse('group_list_all', args=['project', 1])),
            c.post(reverse('link_list', args=['project', 1, 'task'])),
            c.post(reverse('note_list', args=['project', 1])),
            c.post(reverse('object_link_list', args=['project', 1])),
            c.post(reverse('query_bug_client', args=['project', 1])),
            c.post(reverse('user_list', args=['project', 1])),
            c.post(reverse('user_list_all', args=['project', 1])),
            c.post(reverse('lead_user_list')),
        ]

        # Cheeck the array
        assertRedirectsToLogin(response_array, self)

        print("Non Logged in users redirected when visiting objects (GET)")