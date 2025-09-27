from collections import namedtuple

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

import uuid

# Declaration of Username and Password
username = "admin"
password = "Test1234$"



def login_user(c, self):
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class ApiAdminPermissionTests(APITestCase):
    fixtures = ["NearBeach_basic_setup.json"]
    
    URLTest = namedtuple(
        "URLTest",
        ["url", "data", "status_code", "method"],
        defaults=["", {}, 200, "GET"],
    )

    def setUp(self):
        # Login
        self.credentials = {
            "two_factor_login_view-current_step": "auth",
            "auth-username": username,
            "auth-password": password
        }

        # Set up the client
        self.client = APIClient()
        self.factory = APIRequestFactory()

        login_user(self.client, self)

    def _run_test_array(self, data_list):
        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                if data.method == "GET":
                    response = self.client.get(
                        data.url,
                    )
                elif data.method == "POST":
                    response = self.client.post(
                        data.url,
                        data.data,
                    )
                elif data.method == "PUT":
                    response = self.client.put(
                        data.url,
                        data.data,
                        format="json"
                    )
                elif data.method == "DELETE":
                    response = self.client.delete(
                        data.url,
                        data.data,
                        format="json"
                    )
                else:
                    AssertionError("Method Not allowed in API")

                self.assertEqual(response.status_code, data.status_code)

    def test_api_available_data(self):
        data_list = [
            ################
            # AVAILABLE DATA
            ################
            self.URLTest("/api/v0/available_data/customer_list/?destination=project&location_id=1", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/customer_list?destination=project&location_id=1", {}, 301, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/?destination=project&location_id=2", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/customer_list?destination=project&location_id=2", {}, 301, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/?destination=requirement_item&location_id=1", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/?destination=requirement_item&location_id=2", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/?destination=kanban_board&location_id=1", {}, 400, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/", {}, 400, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/", {"destination": "project", "location_id": 1}, 405, "POST"),
            self.URLTest("/api/v0/available_data/sprint_list/", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/sprint_list/1/", {}, 404, "GET"),
            self.URLTest("/api/v0/available_data/sprint_list/1", {}, 404, "GET"),
            self.URLTest("/api/v0/available_data/sprint_list", {}, 301, "GET"),
            self.URLTest("/api/v0/available_data/sprint_list/", {}, 405, "POST"),
            self.URLTest("/api/v0/available_data/tag_list/", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/tag_list/1", {}, 404, "GET"),
            self.URLTest("/api/v0/available_data/tag_list/1/", {}, 404, "GET"),
            self.URLTest("/api/v0/available_data/tag_list", {}, 301, "GET"),
            self.URLTest("/api/v0/available_data/tag_list/", {}, 405, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_coffee_data(self):
        data_list = [
            ########
            # COFFEE
            ########
            self.URLTest("/api/v0/coffee/", {}, 418, "GET"),
            self.URLTest("/api/v0/coffee/", {}, 418, "POST"),
            self.URLTest("/api/v0/coffee/1/", {}, 418, "GET"),
            self.URLTest("/api/v0/coffee/1/", {}, 418, "PUT"),
            self.URLTest("/api/v0/coffee/1/", {}, 418, "DELETE"),
            self.URLTest("/api/v0/coffee", {}, 301, "GET"),
            self.URLTest("/api/v0/coffee", {}, 301, "POST"),
            self.URLTest("/api/v0/coffee/1", {}, 301, "GET"),
            self.URLTest("/api/v0/coffee/1", {}, 301, "PUT"),
            self.URLTest("/api/v0/coffee/1", {}, 301, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_customer_data(self):
        data_list = [
            ##########
            # CUSTOMER
            ##########
            self.URLTest("/api/v0/organisation/1/customer/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/organisation/1/customer/",
                {
                    "customer_title": 2,
                    "customer_first_name": "Socks",
                    "customer_last_name": "Fluffy Butt",
                    "customer_email": "sock@nearbeach.org",
                    "organisation": 1
                },
                201,
                "POST"
            ),
            self.URLTest("/api/v0/organisation/1/customer/1/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/organisation/1/customer/1/",
                {
                    "customer_title": 2,
                    "customer_first_name": "Socks",
                    "customer_last_name": "Fluffy Butt",
                    "customer_email": "sock@nearbeach.org",
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/organisation/1/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/organisation/1/customer", {}, 301, "GET"),
            self.URLTest("/api/v0/organisation/1/customer", {}, 301, "POST"),
            self.URLTest("/api/v0/organisation/1/customer/1", {}, 301, "GET"),
            self.URLTest("/api/v0/organisation/1/customer/1", {}, 301, "PUT"),
            self.URLTest("/api/v0/organisation/1/customer/1", {}, 301, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_kanban_board_data(self):
        data_list = [
            ##############
            # KANBAN BOARD
            ##############
            self.URLTest("/api/v0/kanban_board/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/kanban_board/",
                {
                    "kanban_board_name": "API Kanban Board - " + str(uuid.uuid4()),
                    "group_list": [1, 2],
                    "kanban_column[0]kanban_column_name": "Backlog",
                    "kanban_column[0]kanban_column_property": "Normal",
                    "kanban_column[1]kanban_column_name": "In Progress",
                    "kanban_column[1]kanban_column_property": "Normal",
                    "kanban_column[2]kanban_column_name": "Blocked",
                    "kanban_column[2]kanban_column_property": "Blocked",
                    "kanban_column[3]kanban_column_name": "Review and QA",
                    "kanban_column[3]kanban_column_property": "Normal",
                    "kanban_column[4]kanban_column_name": "Completed",
                    "kanban_column[4]kanban_column_property": "Closed",
                    "kanban_level[0]kanban_level_name": "Swim Lane 1",
                    "kanban_level[1]kanban_level_name": "Swim Lane 2",
                },
                201,
                "POST"
            ),
            self.URLTest("/api/v0/kanban_board/1/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/2/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/kanban_board/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/kanban_board", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board", {}, 301, "POST"),
            self.URLTest("/api/v0/kanban_board/1", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/2", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/1", {}, 301, "PUT"),
            self.URLTest("/api/v0/kanban_board/2", {}, 301, "PUT"),
            self.URLTest("/api/v0/kanban_board/1", {}, 301, "DELETE"),
            self.URLTest("/api/v0/kanban_board/2", {}, 301, "DELETE"),
            self.URLTest("/api/v0/kanban_board/1/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/1/group_and_user/", {"group_list": 2, "user_list": 2}, 201, "POST"),
            # TODO - 0.32 - Rewrite these once we have applied the object_assignment_id into the data
            # self.URLTest(
            #     "/api/v0/kanban_board/1/group_and_user/0/",
            #     {
            #         "user": 2,
            #     },
            #     204,
            #     "DELETE"
            # ),
            # self.URLTest(
            #     "/api/v0/kanban_board/1/group_and_user/0/",
            #     {
            #         "group": 2,
            #     },
            #     204,
            #     "DELETE"
            # ),
            # self.URLTest(
            #     "/api/v0/kanban_board/1/group_and_user/0/",
            #     {
            #         "group": 1,
            #     },
            #     403,
            #     "DELETE"
            # ),
            self.URLTest("/api/v0/kanban_board/2/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/2/group_and_user/", {"group_list": 3}, 201, "POST"),
            # TODO - 0.32 - Currently missing the object_assignment_id, will need to write these in after we deploy that
            # self.URLTest(
            #     "/api/v0/kanban_board/2/group_and_user/0/",
            #     {
            #         "user": 2,
            #     },
            #     204,
            #     "DELETE"
            # ),
            # self.URLTest(
            #     "/api/v0/kanban_board/2/group_and_user/0/",
            #     {
            #         "group": 1,
            #     },
            #     204,
            #     "DELETE"
            # ),
        ]

        self._run_test_array(data_list)

    def test_api_kanban_card_data(self):
        data_list = [
            #############
            # KANBAN CARD
            #############
            self.URLTest("/api/v0/kanban_board/1/kanban_card/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/1/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/2/", {}, 200, "GET"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/1", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/2", {}, 301, "GET"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/2/", {}, 404, "GET"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/1/", {}, 404, "GET"),
            self.URLTest(
                "/api/v0/kanban_board/1/kanban_card/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description":"I created this by the api. :D",
                    "kanban_card_priority": 1,
                    "kanban_column": 3,
                    "kanban_level": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/kanban_board/2/kanban_card/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description": "I created this by the api. :D",
                    "kanban_card_priority": 2,
                    "kanban_column": 6,
                    "kanban_level": 3,
                },
                201,
                "POST",
            ),
            # TODO - Move these tests to specific kanban card tests, as it does not really test permissions here.
            self.URLTest(
                "/api/v0/kanban_board/1/kanban_card/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description": "I created this by the api. :D",
                    "kanban_card_priority": 1,
                    "kanban_column": 300,
                    "kanban_level": 100,
                },
                400,
                "POST",
            ),
            self.URLTest(
                "/api/v0/kanban_board/2/kanban_card/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description": "I created this by the api. :D",
                    "kanban_card_priority": 2,
                    "kanban_column": 50,
                    "kanban_level": 300,
                },
                400,
                "POST",
            ),
            self.URLTest(
                "/api/v0/kanban_board/1/kanban_card/3/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description": "I created this by the api. :D",
                    "kanban_card_priority": 1,
                    "kanban_column": 3,
                    "kanban_level": 1,
                },
                200,
                "PUT",
            ),
            self.URLTest(
                "/api/v0/kanban_board/2/kanban_card/4/",
                {
                    "kanban_card_text": "Created via the api",
                    "kanban_card_description": "I created this by the api. :D",
                    "kanban_card_priority": 2,
                    "kanban_column": 6,
                    "kanban_level": 3,
                },
                200,
                "PUT",
            ),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/3/", {}, 400, "PUT"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/4/", {}, 400, "PUT"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/3", {}, 301, "POST"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/4", {}, 301, "POST"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/3/", {}, 404, "DELETE"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/4/", {}, 404, "DELETE"),
            self.URLTest("/api/v0/kanban_board/1/kanban_card/3/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/kanban_board/2/kanban_card/4/", {}, 204, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_organisation_data(self):
        data_list = [
            ##############
            # ORGANISATION
            ##############
            self.URLTest("/api/v0/organisation/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/organisation/",
                {
                    "organisation_name": "Far Desert",
                    "organisation_email": "support@fardesert.com",
                    "organisation_website": "https://fardesert.com",
                },
                201,
                "POST"
            ),
            self.URLTest("/api/v0/organisation/1/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/organisation/1/",
                {
                    "organisation_name": "Far Desert",
                    "organisation_email": "support@fardesert.com",
                    "organisation_website": "https://fardesert.com",
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/organisation/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/organisation", {}, 301, "GET"),
            self.URLTest("/api/v0/organisation", {}, 301, "POST"),
            self.URLTest("/api/v0/organisation/1", {}, 301, "GET"),
            self.URLTest("/api/v0/organisation/1", {}, 301, "PUT"),
            self.URLTest("/api/v0/organisation/1", {}, 301, "DELETE"),
            self.URLTest("/api/v0/organisation/1/note/", {}, 200, "GET"),
            self.URLTest("/api/v0/organisation/1/note/", {"object_note": "Hello World"}, 201, "POST"),
            # TODO - Expand the above note tests, we'll need to test;
            # 1. Deleting/Editing another users note will fail
            # 2. Can not delete already deleted notes
            # 3. Incorrect object to delete note from
            # 4. Once the PUT method has been implemented, having a user create a note
            # 5. Create notes on Organisations for the users to delete
            # 6. Create an organisation
            # 7. Delete an organisation
            # TAGS
            self.URLTest("/api/v0/organisation/1/tag/", {}, 200, "GET"),
            self.URLTest("/api/v0/organisation/1/tag/", {"tag_id": 1}, 201, "POST"),
            self.URLTest("/api/v0/organisation/1/tag/13/", {}, 204, "DELETE"),
            # TODO - Expand the above tag tests, we'll need to test;
            # 1. Deleting/Editing another objects tags - this should fail
            # 2. PUT method does not exist
            # 3. Create a tag and then delete said tag
        ]

        self._run_test_array(data_list)

    def test_api_project_data(self):
        data_list = [
            #########
            # PROJECT
            #########
            self.URLTest("/api/v0/project/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/project/",
                {
                    "project_name": "API Project",
                    "project_description": "<p>Hello World</p>",
                    "project_start_date": "2024-12-19T15:49:37Z",
                    "project_end_date": "2024-12-19T15:49:37Z",
                    "organisation": 1,
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/project/1/",
                {
                    "project_name": "API Project updated",
                    "project_description": "<p>Hello World again</p>",
                    "project_start_date": "2024-12-19T15:49:37Z",
                    "project_end_date": "2024-12-19T15:49:37Z",
                    "project_status": 2,
                    "project_priority": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest(
                "/api/v0/project/2/",
                {
                    "project_name": "API Project updated",
                    "project_description": "<p>Hello World again</p>",
                    "project_start_date": "2024-12-19T15:49:37Z",
                    "project_end_date": "2024-12-19T15:49:37Z",
                    "project_status": 2,
                    "project_priority": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/project/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/project/1/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/project/2/group_and_user/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/project/1/group_and_user/",
                {
                    "group_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/project/2/group_and_user/",
                {
                    "group_list": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/project/1/group_and_user/",
                {
                    "user_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/project/2/group_and_user/",
                {
                    "user_list": 1,
                },
                201,
                "POST",
            ),
            # TODO - 0.32 - Write the delete functionality for both users and groups. Waiting for the object_assignment_id to pass through into the GET data
            ######################
            # Project - Link tests
            ######################
            self.URLTest('/api/v0/project/1/link/', {}, 200, "GET"),
            self.URLTest('/api/v0/project/1/link/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/project/1/link/',
                {
                    "object_id": 2,
                    "object_type": "task",
                    "object_relation": "blocked_by",
                },
                201,"POST"
            ),
            self.URLTest(
                '/api/v0/project/1/link/',
                {
                    "object_id": 2,
                    "object_type": "task",
                    "object_relation": "blocked_by",
                },
                201, "POST"
            ),
            self.URLTest('/api/v0/project/2/link/43/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/project/1/link/46/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/project/1/link/43/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/project/2/link/46/', {}, 204, "DELETE"),
            # TODO - Create more links against all objects, currently can not test as there is nothing to test but create
            # note tests
            self.URLTest('/api/v0/project/1/note/', {}, 200, "GET"),
            self.URLTest('/api/v0/project/2/note/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/project/1/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/project/2/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/project/1/note/2/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest(
                '/api/v0/project/2/note/3/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest('/api/v0/project/1/note/2/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/project/2/note/3/', {}, 204, "DELETE"),
            # object_sprint tests
            # TODO - 0.32 - Add more sprints to objects for Unit Testing
            # tag tests
        ]

        self._run_test_array(data_list)

    def test_api_requirement_data(self):
        data_list = [
            #########
            # REQUIREMENT
            #########
            self.URLTest("/api/v0/requirement/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/requirement/",
                {
                    "requirement_title": "API Requirement",
                    "requirement_scope": "<p>Hello World</p>",
                    "requirement_type": 1,
                    "requirement_status": 2,
                    "organisation": 1,
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/requirement/1/",
                {
                    "requirement_title": "API Requirement updated",
                    "requirement_scope": "<p>Hello World again</p>",
                    "requirement_type": 2,
                    "requirement_status": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest(
                "/api/v0/requirement/2/",
                {
                    "requirement_title": "API Requirement updated",
                    "requirement_scope": "<p>Hello World again</p>",
                    "requirement_type": 2,
                    "requirement_status": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/requirement/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/requirement/1/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/requirement/2/group_and_user/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/requirement/1/group_and_user/",
                {
                    "group_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/requirement/2/group_and_user/",
                {
                    "group_list": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/requirement/1/group_and_user/",
                {
                    "user_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/requirement/2/group_and_user/",
                {
                    "user_list": 1,
                },
                201,
                "POST",
            ),
            # TODO - 0.32 - Write the delete functionality for both users and groups. Waiting for the object_assignment_id to pass through into the GET data
            ######################
            # Requirement - Link tests
            ######################
            self.URLTest('/api/v0/requirement/1/link/', {}, 200, "GET"),
            self.URLTest('/api/v0/requirement/1/link/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/requirement/1/link/',
                {
                    "object_id": 2,
                    "object_type": "task",
                    "object_relation": "blocked_by",
                },
                201, "POST"
            ),
            self.URLTest(
                '/api/v0/requirement/1/link/',
                {
                    "object_id": 2,
                    "object_type": "task",
                    "object_relation": "blocked_by",
                },
                201, "POST"
            ),
            self.URLTest('/api/v0/requirement/2/link/40/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/requirement/1/link/41/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/requirement/1/link/40/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/requirement/2/link/41/', {}, 204, "DELETE"),
            # TODO - Create more links against all objects, currently can not test as there is nothing to test but create
            # note tests
            self.URLTest('/api/v0/requirement/1/note/', {}, 200, "GET"),
            self.URLTest('/api/v0/requirement/2/note/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/requirement/1/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/requirement/2/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/requirement/1/note/4/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest(
                '/api/v0/requirement/2/note/11/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest('/api/v0/requirement/1/note/4/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/requirement/2/note/11/', {}, 204, "DELETE"),
            # object_sprint tests
            # TODO - 0.32 - Add more sprints to objects for Unit Testing
            # tag tests
        ]

        self._run_test_array(data_list)

    def test_api_request_for_change_data(self):
        data_list = [
            #########
            # REQUEST FOR CHANGE
            #########
            self.URLTest("/api/v0/request_for_change/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/request_for_change/",
                {
                    "rfc_version_number": "0.32.0",
                    "rfc_title": "Release of 0.32.0",
                    "rfc_summary": "<p>Hello World</p>",
                    "rfc_type": 1,
                    "rfc_risk_and_impact_analysis": "Risk and Impact Analysis",
                    "rfc_implementation_plan": "Implementation Plan",
                    "rfc_backout_plan": "Backout Plan",
                    "rfc_test_plan": "Test Plan",
                    "rfc_lead": 1,
                    "rfc_priority": 1,
                    "rfc_risk": 1,
                    "rfc_impact": 1,
                    "organisation": 1,
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/request_for_change/1/",
                {
                    "rfc_version_number": "0.32.0",
                    "rfc_title": "Release of 0.32.0",
                    "rfc_summary": "<p>Hello World</p>",
                    "rfc_type": 1,
                    "rfc_risk_and_impact_analysis": "Risk and Impact Analysis",
                    "rfc_implementation_plan": "Implementation Plan",
                    "rfc_backout_plan": "Backout Plan",
                    "rfc_test_plan": "Test Plan",
                    "rfc_implementation_release_date": "2025-09-26T10:28:32.906Z",
                    "rfc_lead": 1,
                    "rfc_priority": 1,
                    "rfc_risk": 1,
                    "rfc_impact": 1,
                    "organisation": 1,
                    "group_list": [1, 2],

                },
                200,
                "PUT"
            ),
            self.URLTest(
                "/api/v0/request_for_change/2/",
                {
                    "rfc_version_number": "0.32.0",
                    "rfc_title": "Release of 0.32.0",
                    "rfc_summary": "<p>Hello World</p>",
                    "rfc_type": 1,
                    "rfc_risk_and_impact_analysis": "Risk and Impact Analysis",
                    "rfc_implementation_plan": "Implementation Plan",
                    "rfc_backout_plan": "Backout Plan",
                    "rfc_test_plan": "Test Plan",
                    "rfc_implementation_release_date": "2025-09-26T10:28:32.906Z",
                    "rfc_lead": 1,
                    "rfc_priority": 1,
                    "rfc_risk": 1,
                    "rfc_impact": 1,
                    "organisation": 1,
                    "group_list": [1, 2],
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/request_for_change/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/request_for_change/1/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/request_for_change/2/group_and_user/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/request_for_change/1/group_and_user/",
                {
                    "group_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/request_for_change/2/group_and_user/",
                {
                    "group_list": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/request_for_change/1/group_and_user/",
                {
                    "user_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/request_for_change/2/group_and_user/",
                {
                    "user_list": 1,
                },
                201,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_request_for_change_change_task_data(self):
        data_list = [
            self.URLTest("/api/v0/request_for_change/1/change_task/", {}, 200, "GET"),
            self.URLTest("/api/v0/request_for_change/2/change_task/", {}, 200, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task", {}, 301, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task", {}, 301, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task/1/", {}, 200, "GET"),
            self.URLTest("/api/v0/request_for_change/2/change_task/2/", {}, 200, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task/1", {}, 301, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task/2", {}, 301, "GET"),
            self.URLTest("/api/v0/request_for_change/1/change_task/2/", {}, 404, "GET"),
            self.URLTest("/api/v0/request_for_change/2/change_task/1/", {}, 404, "GET"),
            self.URLTest(
                "/api/v0/request_for_change/1/change_task/",
                {
                    "change_task_assigned_user": 1,
                    "change_task_qa_user": 2,
                    "change_task_title": "Change Task Title",
                    "change_task_start_date": "2024-12-19T15:49:37Z",
                    "change_task_end_date": "2024-12-19T15:49:37Z",
                    "is_downtime": "true",
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/request_for_change/2/change_task/",
                {
                    "change_task_assigned_user": 1,
                    "change_task_qa_user": 2,
                    "change_task_title": "Change Task Title",
                    "change_task_start_date": "2024-12-19T15:49:37Z",
                    "change_task_end_date": "2024-12-19T15:49:37Z",
                    "is_downtime": "true",
                },
                201,
                "POST"
            ),
            self.URLTest("/api/v0/request_for_change/1/change_task", {}, 301, "POST"),
            self.URLTest("/api/v0/request_for_change/2/change_task", {}, 301, "POST"),
            self.URLTest(
                "/api/v0/request_for_change/1/change_task/3/",
                {
                    "change_task_assigned_user": 1,
                    "change_task_qa_user": 2,
                    "change_task_title": "Change Task Title",
                    "change_task_start_date": "2024-12-19T15:49:37Z",
                    "change_task_end_date": "2024-12-19T15:49:37Z",
                    "is_downtime": "true",
                },
                200,
                "PUT"
            ),
            self.URLTest(
                "/api/v0/request_for_change/2/change_task/4/",
                {
                    "change_task_assigned_user": 1,
                    "change_task_qa_user": 2,
                    "change_task_title": "Change Task Title",
                    "change_task_start_date": "2024-12-19T15:49:37Z",
                    "change_task_end_date": "2024-12-19T15:49:37Z",
                    "is_downtime": "true",
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/request_for_change/2/change_task/1/", {}, 404, "DELETE"),
            self.URLTest("/api/v0/request_for_change/1/change_task/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v0/request_for_change/1/change_task/1", {}, 301, "DELETE"),
            self.URLTest("/api/v0/request_for_change/2/change_task/2", {}, 301, "DELETE"),
            self.URLTest("/api/v0/request_for_change/1/change_task/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/request_for_change/2/change_task/2/", {}, 204, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_sprint_data(self):
        data_list = [
            ###############
            # SPRINT DATA #
            ###############
            self.URLTest("/api/v0/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v0/sprint/1/", {}, 200, "GET"),
            self.URLTest("/api/v0/sprint/2/", {}, 200, "GET"),
            self.URLTest("/api/v0/sprint/", {
                "destination": "project",
                "location_id": 1,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 201, "POST"),
            self.URLTest("/api/v0/sprint/", {
                "destination": "project",
                "location_id": 2,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 201, "POST"),
            self.URLTest("/api/v0/sprint/", {
                "destination": "requirement",
                "location_id": 1,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 201, "POST"),
            self.URLTest("/api/v0/sprint/", {
                "destination": "requirement",
                "location_id": 2,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 201, "POST"),
            self.URLTest("/api/v0/sprint/1/", {
                "destination": "project",
                "location_id": 1,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 200, "PUT"),
            self.URLTest("/api/v0/sprint/2/", {
                "destination": "project",
                "location_id": 2,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 200, "PUT"),
            self.URLTest("/api/v0/sprint/1/", {
                "destination": "project",
                "location_id": 2,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 404, "PUT"),
            self.URLTest("/api/v0/sprint/2/", {
                "destination": "project",
                "location_id": 1,
                "sprint_name": "Hello Sprint World",
                "sprint_start_date": "2024-12-19T15:49:37Z",
                "sprint_end_date": "2024-12-19T15:49:37Z",
            }, 404, "PUT"),
            self.URLTest("/api/v0/sprint/1/", {
                "destination": "project",
                "location_id": 2,
            }, 404, "DELETE"),
            self.URLTest("/api/v0/sprint/2/", {
                "destination": "project",
                "location_id": 1,
            }, 404, "DELETE"),
            self.URLTest("/api/v0/sprint/1/", {
                "destination": "project",
                "location_id": 1,
            }, 204, "DELETE"),
            self.URLTest("/api/v0/sprint/2/", {
                "destination": "project",
                "location_id": 2,
            }, 204, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_task_data(self):
        data_list = [
            #########
            # TASK
            #########
            self.URLTest("/api/v0/task/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/task/",
                {
                    "task_short_description": "API Task",
                    "task_long_description": "<p>Hello World</p>",
                    "task_start_date": "2024-12-19T15:49:37Z",
                    "task_end_date": "2024-12-19T15:49:37Z",
                    "organisation": 1,
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/task/1/",
                {
                    "task_short_description": "API Task updated",
                    "task_long_description": "<p>Hello World again</p>",
                    "task_start_date": "2024-12-19T15:49:37Z",
                    "task_end_date": "2024-12-19T15:49:37Z",
                    "task_status": 2,
                    "task_priority": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest(
                "/api/v0/task/2/",
                {
                    "task_short_description": "API Task updated",
                    "task_long_description": "<p>Hello World again</p>",
                    "task_start_date": "2024-12-19T15:49:37Z",
                    "task_end_date": "2024-12-19T15:49:37Z",
                    "task_status": 2,
                    "task_priority": 2,
                },
                200,
                "PUT"
            ),
            self.URLTest("/api/v0/task/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v0/task/1/group_and_user/", {}, 200, "GET"),
            self.URLTest("/api/v0/task/2/group_and_user/", {}, 200, "GET"),
            self.URLTest(
                "/api/v0/task/1/group_and_user/",
                {
                    "group_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/task/2/group_and_user/",
                {
                    "group_list": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/task/1/group_and_user/",
                {
                    "user_list": 2,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v0/task/2/group_and_user/",
                {
                    "user_list": 1,
                },
                201,
                "POST",
            ),
            # TODO - 0.32 - Write the delete functionality for both users and groups. Waiting for the object_assignment_id to pass through into the GET data
            ######################
            # Task - Link tests
            ######################
            self.URLTest('/api/v0/task/1/link/', {}, 200, "GET"),
            self.URLTest('/api/v0/task/1/link/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/task/1/link/',
                {
                    "object_id": 2,
                    "object_type": "requirement",
                    "object_relation": "blocked_by",
                },
                201, "POST"
            ),
            self.URLTest(
                '/api/v0/task/1/link/',
                {
                    "object_id": 2,
                    "object_type": "requirement",
                    "object_relation": "blocked_by",
                },
                201, "POST"
            ),
            self.URLTest('/api/v0/task/2/link/43/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/task/1/link/44/', {}, 400, "DELETE"),
            self.URLTest('/api/v0/task/1/link/43/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/task/2/link/44/', {}, 204, "DELETE"),
            # TODO - Create more links against all objects, currently can not test as there is nothing to test but create
            # note tests
            self.URLTest('/api/v0/task/1/note/', {}, 200, "GET"),
            self.URLTest('/api/v0/task/2/note/', {}, 200, "GET"),
            self.URLTest(
                '/api/v0/task/1/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/task/2/note/',
                {
                    "object_note": "<p>Hello World</p>",
                },
                201,
                "POST",
            ),
            self.URLTest(
                '/api/v0/task/1/note/5/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest(
                '/api/v0/task/2/note/8/',
                {
                    "object_note": "<h1>Hello World Updated</h1>",
                },
                200,
                "PUT",
            ),
            self.URLTest('/api/v0/task/1/note/5/', {}, 204, "DELETE"),
            self.URLTest('/api/v0/task/2/note/8/', {}, 204, "DELETE"),
            # object_sprint tests
            # TODO - 0.32 - Add more sprints to objects for Unit Testing
            # tag tests
        ]

        self._run_test_array(data_list)

    def test_api_user_api_data(self):
        data_list = [
            self.URLTest("/api/v0/user/1/api_key/", {}, 200, "GET"),
            self.URLTest("/api/v0/user/1/api_key/", {}, 201, "POST"),
            self.URLTest(
                "/api/v0/user/1/api_key/b171178a441ac13f376013aebb2ec9190b5cd47d9e779f51e59cc33d017924ec170226a87fee8a314a840e80a08b84d76edd9587bbda3ee3b1a3936076f9fe98/", 
                {}, 
                204,
                "DELETE"
            ),
        ]

        self._run_test_array(data_list)

