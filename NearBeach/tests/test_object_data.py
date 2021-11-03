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


class TestObjectData(TestCase):
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': username,
            'password': password
        }

    def test_incorrect_location_data(self):
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse('associated_objects', args=['taks', 1]))
        self.assertEqual(response.status_code, 403)

    def test_team_leader_searches(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Go to an existing customer -> user should have access
        response = c.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
