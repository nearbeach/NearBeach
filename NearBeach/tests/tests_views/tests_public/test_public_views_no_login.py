from django.test import TestCase
from django.urls import reverse
from collections import namedtuple


class PublicViewNoLoginTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def test_public_links_as_open_to_public(self):
        kwargsTest = namedtuple(
            "kwargsTest",
            ["destination","location_id", "public_link_id"],
        )

        data_list = [
            kwargsTest("requirement", 1, "fbda2f94-be7b-41e5-b93a-3ce65516d09d"),
            kwargsTest("requirement", 2, "5435086c-a145-4540-bc71-35a0fd0ee171"),
            kwargsTest("requirement_item", 1, "aba74809-aae5-4fc4-8929-5fd835fefa22"),
            kwargsTest("requirement_item", 2, "9b6a9317-df46-453f-aa5b-6f33b77c28c4"),
            kwargsTest("project", 1, "3d7346c4-05b6-41df-816a-eff814d9bbd0"),
            kwargsTest("project", 2, "5f369dc9-a0bb-416d-9779-92576d0500bb"),
            kwargsTest("task", 1, "1c1067e9-563f-4419-9dac-e87d757ecb37"),
            kwargsTest("task", 2, "c5994697-a7e6-4e54-b8b1-4dee7315d7ea"),
            kwargsTest("kanban_card", 1, "feb8f0e1-369a-4934-8208-9de39f9dfa98"),
            kwargsTest("kanban_board", 1, "755ee6ea-7eac-4e8b-9c19-fbdba2dd290d"),
            kwargsTest("kanban_card", 2, "37a7cf65-c732-4e67-b16f-97d77329bdda"),
            kwargsTest("kanban_board", 2, "57fea1be-1cbb-4583-8381-9609aa58334b"),
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                response = self.client.get(
                    reverse("public_link", kwargs={
                        "destination": data.destination,
                        "location_id": data.location_id,
                        "public_link_id": data.public_link_id
                    }),
                    follow=True,
                )

                self.assertEqual(response.status_code, 200)
