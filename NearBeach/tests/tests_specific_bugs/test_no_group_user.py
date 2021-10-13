from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = 'no_group_user'
password = 'Test1234$'

"""
Method to replicate
~~~~~~~~~~~~~~~~~~~
1. A user that is not associated with any groups tries to login

Expected Results
~~~~~~~~~~~~~~~~
User can not log in
"""


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active is False)


class NewInstanceLoginTest(TestCase):
    fixtures = ['NearBeach_no_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_admin_login(self):
        c = Client()

        # User will be logged in
        login_user(c, self)
