from django.test import TestCase, Client
from django.urls import reverse


class PublicViewNoLoginTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def test_public_links_as_open_to_public(self):
        # Test Project 1
        response = self.client.get(
            reverse("public_link", kwargs={
                "destination": "project",
                "location_id": 1,
                "public_link_id": "3d7346c4-05b6-41df-816a-eff814d9bbd0",
            }),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        # Test Project 2
        response = self.client.get(
            reverse("public_link", kwargs={
                "destination": "project",
                "location_id": 1,
                "public_link_id": "5f369dc9-a0bb-416d-9779-92576d0500bb"
            }),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
