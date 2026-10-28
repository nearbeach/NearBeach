"""/public_link/<id>/ - the page behind a shared link. It needs no log in, but only for links that are active."""
from django.test import Client, TestCase
from django.urls import reverse

from NearBeach.models.misc.misc import PublicLink


class PublicLinkViewTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        self.link = PublicLink.objects.filter(is_deleted=False, is_active=True).first()
        self.assertIsNotNone(self.link, "The fixture needs an active public link")
        self.url = f"/public_link/{self.link.id}/"

    def test_an_active_link_shows_the_page_without_logging_in(self):
        response = Client().get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "NearBeach/public_link/public_link.html")

    def test_an_active_link_also_works_when_logged_in(self):
        client = Client()
        client.login(username="team_leader", password="Test1234$")

        self.assertEqual(client.get(self.url).status_code, 200)

    def test_an_inactive_link_goes_to_the_login_page(self):
        PublicLink.objects.filter(pk=self.link.pk).update(is_active=False)

        response = Client().get(self.url)

        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_a_deleted_link_goes_to_the_login_page(self):
        PublicLink.objects.filter(pk=self.link.pk).update(is_deleted=True)

        response = Client().get(self.url)

        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_an_unknown_link_goes_to_the_login_page(self):
        response = Client().get("/public_link/00000000-0000-4000-8000-000000000000/")

        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_turning_a_link_back_on_makes_it_work_again(self):
        PublicLink.objects.filter(pk=self.link.pk).update(is_active=False)
        self.assertEqual(Client().get(self.url).status_code, 302)

        PublicLink.objects.filter(pk=self.link.pk).update(is_active=True)

        self.assertEqual(Client().get(self.url).status_code, 200)
