from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from rest_framework.test import APIClient, APIRequestFactory
from unittest.mock import patch


class ApiNoGroupPermissionTests(BaseApiClass):
    username = "no_group"
    password = "Test1234$"

    # OVERRIDE
    def setUp(self):
        """Method run on test start-up - sets up the test by logging in and providing the client and factory"""
        self.client = APIClient()
        self.factory = APIRequestFactory()

        # Disable throttling for the auth endpoint during tests
        patcher = patch(
            "NearBeach.views.api_v1.authentication.authentication_api_view.AuthenticationView.throttle_classes",
            [],
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self._login_user()

    # OVERRIDE
    def _login_user(self):
        """Private Method for logging user in"""
        if self.username == "":
            # No username to log in with
            return

        response = self.client.post(
            "/api/v1/authentication/",
            {
                "username": self.username,
                "password": self.password,
                "otp_token": ""
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 401)

    def test_api_permissions_no_group_project(self):
        """Test - API No Group Permissions for Project"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/6/", {}, 403, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/",
                {
                    "title": "New API Project Title",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/",
                {
                    "title": "New API Project Title",
                },
                403,
                "PATCH",
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [1, 2],
                },
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [1],
                },
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [2],
                },
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [3],
                },
                403,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 403, "DELETE"),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/6/",
                {
                    "title": "New API Project Title",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/9999/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
    

    def test_api_permissions_no_group_project_customers(self):
        """Test - API Admin Permissions for the Project customers submodule"""
        data_list = [
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),

            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/customer/", {}, 403, "GET"),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/customer/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/customer/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/customer/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_documentation(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/documents/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/documents/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/documents/", {}, 403, "GET"),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/3/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/3/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/1/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/277b25be-7913-4432-968f-fa3c699956f3/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/5390175c-82e6-47cb-b9ae-91d88a323868/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/3/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/17f494c7-067e-4f70-b944-64439d9101a7/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/93ac2002-ff86-4835-9607-65037279c8b9/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/3/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/17f494c7-067e-4f70-b944-64439d9101a7/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/277b25be-7913-4432-968f-fa3c699956f3/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/5390175c-82e6-47cb-b9ae-91d88a323868/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/93ac2002-ff86-4835-9607-65037279c8b9/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/1/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/10/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_groups(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/groups/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/groups/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/groups/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/groups/",
                {
                    "group_list": [1],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/groups/",
                {
                    "group_list": [1],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/groups/",
                {
                    "group_list": [1],
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/groups/1/",
                {},
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/groups/1/",
                {},
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/groups/1/",
                {},
                403,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_links(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/link_list/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/link_list/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/link_list/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/link_list/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/link_list/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/link_list/43/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/47/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/link_list/43/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/link_list/48/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/43/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/link_list/43/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/link_list/47/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/link_list/43/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/link_list/48/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/link_list/43/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_notes(self):
        """Test - API Admin Permissions for the Project Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/notes/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/notes/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/notes/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/notes/",
                {
                    "note": "Hello World",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/",
                {
                    "note": "Hello World",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/notes/",
                {
                    "note": "Hello World",
                },
                403,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/notes/2/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/3/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/notes/3/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/2/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/notes/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/notes/3/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/notes/3/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/notes/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_organisation(self):
        """Test - API Admin Permissions for the Project organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/organisation/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/organisation/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/organisation/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/organisation/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/organisation/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/organisation/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_public_link(self):
        """Test - API Admin Permissions for the Project public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/public_link/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/public_link/",
                {},
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/",
                {},
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/public_link/",
                {},
                403,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_sprint_links(self):
        """Test - API Admin Permissions for the Project sprint link module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/sprint/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/sprint/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/3/sprint/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/1/sprint/",
                {
                    "title": "API Sprint",
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/sprint/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/sprint/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/sprint/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/sprint/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/sprint/1/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_project_user_list(self):
        """Test - API Admin Permissions for the Project user list module"""
        data_list = [
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/users/",
                {
                    "user_list": [1],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/users/",
                {
                    "user_list": [2, 3],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/users/",
                {
                    "user_list": [2, 3],
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/users/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/users/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/3/users/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/1/users/5/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
