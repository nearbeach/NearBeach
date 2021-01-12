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

