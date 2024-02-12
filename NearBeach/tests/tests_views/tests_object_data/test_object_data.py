from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "team_leader"
password = "Test1234$"
long_string = """
    There once was a cat called Socks, she liked to eat treats whilst on stream. People liked to feed her treats because
    she was adoriable. Currently she is licking my arm, I think because she enjoyed the treats she got on stream. Socks
    does like to every now and then meow into the microphone.
"""


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class TestObjectData(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        self.credentials = {"username": username, "password": password}

    def test_incorrect_destination_data(self):
        """
        The following test will make sure;
        1. Each of the Object data functions that has destinations has the decorator @check_destination
        2. Make sure the @check_destination works
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # List or URLS
        url_list = [
            "add_bug",
            "add_customer",
            "add_group",
            "add_link",
            "add_notes",
            "add_tags",
            "add_user",
            "associated_objects",
            "bug_list",
            "customer_list",
            "customer_list_all",
            # "group_list",
            # "group_list_all",
            "note_list",
            "object_link_list",
            "query_bug_client",
            "remove_group",
            "remove_link",
            "remove_user",
            "tag_list",
            "user_list",
            # "user_list_all",
        ]

        # Loop through each url to test to make sure the decorator is applied
        for url in url_list:
            with self.subTest(url):
                # Get data of wrong location - gets a 403
                response = c.post(reverse(url, args=["task", 1]))
                self.assertEqual(response.status_code, 403)

    def test_incorrect_destination_data__link_list(self):
        """
        The following test will make sure;
        1. Link List functions has the decorator @check_destination
        2. Make sure the @check_destination works
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("link_list", args=["task", 1, "project"]))
        self.assertEqual(response.status_code, 403)

    def test_correct_destination_data__link_list(self):
        """
        The following test will make sure;
        1. Link List functions has the decorator @check_destination
        2. Make sure the @check_destination works
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # Get data of wrong location - gets a 403
        response = c.post(reverse("link_list", args=["task", 2, "project"]))
        self.assertEqual(response.status_code, 200)

    def test_correct_object_data__without_forms(self):
        """
        The following test will make sure;
        1. Each object data function will work correctly when given the correct;
            b. Description
            c. Location
        Form data is not required for these tests.
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # List or URLS
        url_list = [
            "associated_objects",
            "bug_list",
            "customer_list",
            "customer_list_all",
            # "group_list",
            # "group_list_all",
            "note_list",
            "object_link_list",
            "tag_list",
            "user_list",
            # "user_list_all",
        ]

        # Loop through each url to test to make sure the decorator is applied
        for url in url_list:
            with self.subTest(url):
                # Get data of wrong location - gets a 403
                response = c.post(reverse(url, args=["task", 2]))
                self.assertEqual(response.status_code, 200)

    def test_correct_object_data__without_forms_and_args(self):
        """
        The following test will make sure;
        1. Each object data function will work correctly when given the correct;
            b. Description
            c. Location
        Form data is not required for these tests.
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # List or URLS
        url_list = [
            "bug_client_list",
            "tag_list_all",
        ]

        # Loop through each url to test to make sure the decorator is applied
        for url in url_list:
            with self.subTest(url):
                # Get data of wrong location - gets a 403
                response = c.post(reverse(url))
                self.assertEqual(response.status_code, 200)

    def test_correct_object_data__with_forms(self):
        """
        The following test will make sure;
        1. Each object data function will work correctly when given the correct;
            a. Form data
            b. Description
            c. Location
        """
        c = Client()

        # User wil be logged in
        login_user(c, self)

        # List or URLS
        data_list = [
            {
                "url": "add_bug",
                "formData": {
                    "bug_client": 1,
                    "bug_id": 1,
                    "bug_description": "Test",
                    "bug_status": "In Progress"
                }
            },
            {"url": "add_tags", "formData": {"tag_id": 1}},
            {"url": "add_customer", "formData": {"customer": 1}},
            {"url": "add_group", "formData": {"group_list": [1, 2]}},
            {
                "url": "add_link",
                "formData": {
                    "project": "2",
                    "object_relation": "blocked_by",
                },
            },
            {"url": "add_notes", "formData": {"note": "<p>Add a note</p>"}},
            {"url": "add_user", "formData": {"user_list": [1, 2, 3]}},
            {"url": "remove_group", "formData": {"group_id": 1}},
            {"url": "remove_user", "formData": {"username": "admin"}},
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                # Get data of wrong location - gets a 403
                response = c.post(
                    reverse(data["url"], args=["task", 2]), data["formData"]
                )
                self.assertEqual(response.status_code, 200)
