from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from NearBeach.views.search_views import search

# Declaration of Username and Password
username = 'team_leader'
password = 'Test1234$'
long_string = """
    There once was a cat called Socks, she liked to eat treats whilst on stream. People liked to feed her treats because
    she was adoriable. Currently she is licking my arm, I think because she enjoyed the treats she got on stream. Socks
    does like to every now and then meow into the microphone.
"""

def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


class TeamLeaderSearchTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_team_leader_searches(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        response = c.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search
        response = c.post(
            reverse('search'),
            {
                'search': 'RFC',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search a number
        response = c.post(
            reverse('search'),
            {
                'search': 2,
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search for closed items
        response = c.post(
            reverse('search'),
            {
                'search': 'RFC',
                'include_closed': True,
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search for a string that is > 250 character.
        # This test should fail
        # response = c.post(
        #     reverse('search'),
        #     {
        #         'search': long_string,
        #     }
        # )
        # self.assertEqual(response.status_code, 400)

    def test_team_leader_searches_api(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        response = c.get(reverse('search_data'))
        self.assertEqual(response.status_code, 405)

        # Use the search bar to search
        response = c.post(
            reverse('search'),
            {
                'search': 'RFC',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search a number
        response = c.post(
            reverse('search_data'),
            {
                'search': 2,
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search for closed items
        response = c.post(
            reverse('search_data'),
            {
                'search': 'RFC',
                'include_closed': True,
            }
        )
        self.assertEqual(response.status_code, 200)

        # Use the search bar to search for a string that is > 250 character.
        # This test should fail
        response = c.post(
            reverse('search_data'),
            {
                'search': long_string,
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_team_leader_searches_customers(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        response = c.get(reverse('search_customer'))
        self.assertEqual(response.status_code, 200)

        # Team leader uses the API to get customer details
        response = c.post(
            reverse('search_customer_data'),
            {
                'search': "NearBeach",
            }
        )
        self.assertEqual(response.status_code, 200)

        # TODO: Add in the UNIT TESTS for testing data in produces certain data out

    def test_team_leader_searches_organisations(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        response = c.get(reverse('search_organisation'))
        self.assertEqual(response.status_code, 200)

        # Team leader uses the API to get customer details
        response = c.post(
            reverse('search_organisation_data'),
            {
                'search': "NearBeach",
            }
        )
        self.assertEqual(response.status_code, 200)

        # TODO: Add in the UNIT TESTS for testing data in produces certain data out

