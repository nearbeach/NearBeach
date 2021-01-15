from django.test import TestCase, Client
from django.urls import reverse

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
        self.assertEqual(response.status_code,200)
        print("Non logged in users can get access to the login page")


class CheckCustomerInformation(TestCase):
    def test_customer_information_page(self):
        # Make sure the customer information page redirects
        c = Client()
        response_get = c.get(reverse('customer_information', args = [1]))
        response_post = c.post(reverse('customer_information_save',args = [1]))

        # Check
        self.assertRedirects(
            response_get,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        # Notify tester
        print("Non logged in users get redirected when visiting customers")

class CheckDashboard(TestCase):
    def test_dashboard(self):
        # Make sure the user gets redirected to the login page
        c = Client()
        response_get = c.get(reverse('dashboard'))
        response_post_bug_list = c.get(reverse('get_bug_list'))
        response_post_get_my_objects = c.get(reverse('get_my_objects'))

        # Check
        self.assertRedirects(
            response_get,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        
        self.assertRedirects(
            response_post_bug_list,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_get_my_objects,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        # Tell tester of results
        print("Non Logged in users redirected when visiting dashboard")


class CheckDocumentation(TestCase):
    def test_documentation(self):
        # Make sure the user gets redirected to the login page
        c = Client()
        
        # The get components should receive a 405
        response_get_add_folder = c.get(reverse('document_add_folder',args=['project',1]))
        response_get_add_link = c.get(reverse('document_add_link', args=['project',1]))
        response_get_list_files = c.get(reverse('document_list_files', args=['project',1]))
        response_get_list_folders = c.get(reverse('document_list_folders', args=['project',1]))
        response_get_upload = c.get(reverse('document_upload', args=['project',1]))
        response_get_max_upload = c.get(reverse('document_get_max_upload'))
        
        # The POST components should be redirected
        response_post_add_folder = c.post(reverse('document_add_folder', args=['project',1]))
        response_post_add_link = c.post(reverse('document_add_link', args=['project',1]))
        response_post_list_files = c.post(reverse('document_list_files', args=['project',1]))
        response_post_list_folders = c.post(reverse('document_list_folders', args=['project',1]))
        response_post_upload = c.post(reverse('document_upload', args=['project',1]))
        response_post_max_upload = c.post(reverse('document_get_max_upload'))

        # The get components should receive a 405
        self.assertEqual(response_get_add_folder.status_code,405)
        self.assertEqual(response_get_add_link.status_code,405)
        self.assertEqual(response_get_list_files.status_code,405)
        self.assertEqual(response_get_list_folders.status_code,405)
        self.assertEqual(response_get_upload.status_code,405)
        self.assertEqual(response_get_max_upload.status_code,405)

        # The post components should be redirected

        self.assertRedirects(
            response_post_add_folder,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_add_link,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_list_files,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_list_folders,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_upload,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_max_upload,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        print("Non Logged in users redirected when visiting documentation")


class CheckKanban(TestCase):
    def test_kanban_information(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        response_get_information = c.get(reverse('kanban_information', args=[1]))
        response_get_information_add_link = c.get(reverse('add_kanban_link', args=[1,'project']))
        response_get_information_link_list = c.get(reverse('kanban_link_list', args=[1,'project']))
        response_get_information_new_card = c.get(reverse('new_kanban_card', args=[1]))
        response_get_information_move_card = c.get(reverse('move_kanban_card', args=[1]))
        response_get_information_check_kanban_board_name = c.get(reverse('check_kanban_board_name'))
        response_get_information_check_card = c.get(reverse('kanban_update_card'))


        self.assertRedirects(
            response_get_information,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_add_link,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_link_list,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_new_card,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_move_card,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_check_kanban_board_name,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_get_information_check_card,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        print("Non Logged in users redirected when visiting kanban information")


class CheckPrivateDocument(TestCase):
    def test_private_document(self):
        # Make sure the user gets redirected to the login page
        c = Client()
        response_get = c.get(reverse('private_download_file', args=['12345678-1234-5678-1234-567812345678']))

        self.assertRedirects(
            response_get,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        print("Non Logged in users redirected when visiting private document")

class CheckNew(TestCase):
    def new(self):
        # Make sure the user gets redirected to the login page
        c = Client()
        
        response_get_new_customer = c.get(reverse('new_customer'))
        response_get_new_kanban = c.get(reverse('new_kanban'))
        response_get_new_organisation = c.get(reverse('new_organisation'))
        response_get_new_project = c.get(reverse('new_project'))
        response_get_new_rfc = c.get(reverse('new_request_for_change'))
        response_get_new_requirement = c.get(reverse('new_requirement'))
        response_get_new_requirement_item = c.get(reverse('new_requirement_item', args=[1]))
        response_get_new_task = c.get(reverse('new_task'))
        
        self.assertEqual(response_get_new_customer.status_code,405)
        self.assertEqual(response_get_new_kanban.status_code,405)
        self.assertEqual(response_get_new_organisation.status_code,405)
        self.assertEqual(response_get_new_project.status_code,405)
        self.assertEqual(response_get_new_rfc.status_code,405)
        self.assertEqual(response_get_new_requirement.status_code,405)
        self.assertEqual(response_get_new_requirement_item.status_code,405)
        self.assertEqual(response_get_new_task.status_code,405)

        print("Non Logged in users redirected when visiting private document")
        
    def new_save(self):
        # Make sure the user gets redirected to the login page
        c = Client()

        response_post_new_customer = c.post(reverse('new_customer_save'))
        response_post_new_kanban = c.post(reverse('new_kanban_save'))
        response_post_new_organisation = c.post(reverse('new_organisation_save'))
        response_post_new_project = c.post(reverse('new_project_save'))
        response_post_new_rfc = c.post(reverse('new_request_for_change_save'))
        response_post_new_requirement = c.post(reverse('new_requirement_save'))
        response_post_new_requirement_item = c.post(reverse('new_requirement_item_save', args=[1]))
        response_post_new_task = c.post(reverse('new_task_save'))

        self.assertRedirects(
            response_post_new_customer,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_kanban,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_organisation,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_project,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_rfc,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_requirement,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

        self.assertRedirects(
            response_post_new_requirement_item,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )
        self.assertRedirects(
            response_post_new_task,
            reverse('login'),
            status_code = 302,
            target_status_code = 200,
            msg_prefix = '',
            fetch_redirect_response = True
        )

