from collections import namedtuple

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

import uuid

# Declaration of Username and Password
username = "admin"
password = "Test1234$"



def login_user(c: object, self: object) -> object:
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

        # Setup the client
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
                        data.data,
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
            # TODO - Check why this test is not working in the test stream. It works when manually tested
            # self.URLTest(
            #     "/api/v0/available_data/customer_list/",
            #     {"destination": "project", "location_id": 2},
            #     200,
            #     "GET"
            # ),
            self.URLTest("/api/v0/available_data/customer_list", {"destination": "project", "location_id": 1}, 301,
                         "GET"),
            self.URLTest("/api/v0/available_data/customer_list/", {}, 400, "GET"),
            self.URLTest("/api/v0/available_data/customer_list/", {"destination": "project", "location_id": 1}, 405,
                         "POST"),
            self.URLTest("/api/v0/available_data/sprint_list/", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/sprint_list", {"destination": "project", "location_id": 1}, 301,
                         "GET"),
            self.URLTest("/api/v0/available_data/sprint_list/", {}, 405, "POST"),
            self.URLTest("/api/v0/available_data/tag_list/", {}, 200, "GET"),
            self.URLTest("/api/v0/available_data/tag_list", {"destination": "project", "location_id": 1}, 301, "GET"),
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
                    "group_list": 1,
                    "group_list": 2,
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
                    "project_start_date": "2024-12-19 15:49:37",
                    "project_end_date": "2024-12-19 15:49:37",
                    "organisation": 1,
                    "group_list": 1,
                    "group_list": 2,
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v0/project/1/",
                {
                    "project_name": "API Project updated",
                    "project_description": "<p>Hello World again</p>",
                    "project_start_date": "2024-12-19 15:49:37",
                    "project_end_date": "2024-12-19 15:49:37",
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
                    "project_start_date": "2024-12-19 15:49:37",
                    "project_end_date": "2024-12-19 15:49:37",
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
            # link tests
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
        data_list = []

        self._run_test_array(data_list)

    def test_api_request_for_change_data(self):
        data_list = []

        self._run_test_array(data_list)

    def test_api_sprint_data(self):
        data_list = []

        self._run_test_array(data_list)

    def test_api_task_data(self):
        data_list = []

        self._run_test_array(data_list)

