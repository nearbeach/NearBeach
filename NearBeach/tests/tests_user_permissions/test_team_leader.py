from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = 'team_leader'
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

    #def test_customer_permissions(self):
    #    c = Client()
#
#        # User will be logged in
#        login_user(c, self)
#
#        # Go to an existing customer -> user should have access
#        response = c.get(reverse('customer_information', args=['1']))
#        self.assertEqual(response.status_code, 200)
#
