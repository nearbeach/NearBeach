from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = 'admin'
password = 'Test1234$'

"""
Method to replicate
~~~~~~~~~~~~~~~~~~~
1. Bring up a new instance of NearBeach (grab from fixtures)
2. Try and log in as the admin user

Expected Results
~~~~~~~~~~~~~~~~
User will log in with no issues, system will create all of the user's permission sets and groups
"""


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


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

        # Make sure the admin user can open up the project
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
