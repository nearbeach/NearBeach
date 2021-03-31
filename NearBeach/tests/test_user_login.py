from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogInTest(TestCase):
    fixtures = ['NearBeach_basic_setup.json']
    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'Test1234$'}
        # User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post(
            reverse('login'),
            self.credentials,
            follow=True,
        )
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        print("Tested User Loggin In")