from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAdminPermissionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_project(self):
        """Test - API Admin Permissions for the Project module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/",
                {
                    "title": "New API Project Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/",
                {
                    "title": "New API Project Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/",
                {
                    "title": "New API Project Title",
                },
                404,
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
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [1],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                    "group_list": [3],
                },
                400,
                "POST"
            ),
            # Missing group_list must be a 400, not a 500
            self.URLTest(
                "/api/v1/project/",
                {
                    "title": "API Project",
                },
                400,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 204, "DELETE"),
            # The create tests above have made projects 3+, so use an id that is never reached
            self.URLTest("/api/v1/project/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_customers(self):
        """Test - API Admin Permissions for the Project customers submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/customer/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/customer/",
                {
                    "id": 1,
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/1/customer/2/", {}, 400, "DELETE"),
            self.URLTest("/api/v1/project/2/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/2/customer/2/", {}, 400, "DELETE"),
            self.URLTest("/api/v1/project/3/customer/1/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/project/3/customer/2/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_documentation(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/documents/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                404,
                "POST",
            ),
            # NOTE - we only need to test the folder, as this is a permission check only. Links and Uploads hit the
            # same endpoint. Thus they are not here

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/3/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/documents/3/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                400,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                400,
                "PATCH",
            ),
            # NOTE - we only need to test the folder, as this is a permission check only. Links and Uploads hit the
            # same endpoint. Thus they are not here

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/documents/1/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/277b25be-7913-4432-968f-fa3c699956f3/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/5390175c-82e6-47cb-b9ae-91d88a323868/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/3/",
                {
                    "type": "folder",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/17f494c7-067e-4f70-b944-64439d9101a7/",
                {
                    "type": "document",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/93ac2002-ff86-4835-9607-65037279c8b9/",
                {
                    "type": "link",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/3/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "type": "folder",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/17f494c7-067e-4f70-b944-64439d9101a7/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/277b25be-7913-4432-968f-fa3c699956f3/",
                {
                    "type": "document",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/5390175c-82e6-47cb-b9ae-91d88a323868/",
                {
                    "type": "document",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/1/documents/93ac2002-ff86-4835-9607-65037279c8b9/",
                {
                    "type": "link",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/2/documents/1/",
                {
                    "type": "folder",
                },
                400,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/3/documents/1/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/project/3/documents/10/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_groups(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/groups/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/groups/",
                {
                    "group_list": [1],
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/groups/1/",
                {},
                200,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/groups/1/",
                {},
                200,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/groups/1/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_links(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/link_list/", {}, 404, "GET"),

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
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/link_list/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                404,
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
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/47/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/link_list/43/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/link_list/48/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                400,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/43/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                400,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/link_list/43/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/47/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/link_list/43/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/link_list/48/",
                {},
                400,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/link_list/43/",
                {},
                400,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_misc(self):
        """Test - API Admin Permissions for the Project Misc submodule"""
        # TODO - Complete this after setting up front end
        data_list = [
            #########
            # READ
            #########

            #########
            # CREATE
            #########

            #########
            # UPDATE
            #########

            #########
            # DELETE
            #########
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_notes(self):
        """Test - API Admin Permissions for the Project Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/notes/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/notes/",
                {
                    "note": "Hello World",
                },
                404,
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
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/3/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/notes/3/",
                {
                    "note": "Hello World",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/2/",
                {
                    "note": "Hello World",
                },
                404,
                "PATCH",
            ),
            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/notes/2/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/3/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/notes/3/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/notes/2/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_organisation(self):
        """Test - API Admin Permissions for the Project organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/organisation/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/organisation/",
                {
                    "id": 1,
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/organisation/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/organisation/2/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/organisation/4/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_public_link(self):
        """Test - API Admin Permissions for the Project public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/public_link/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/1/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/public_link/",
                {},
                404,
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
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/3/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {
                    "is_active": "false",
                },
                400,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {
                    "is_active": "false",
                },
                400,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/",
                {},
                400,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/",
                {},
                400,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_sprint_links(self):
        """Test - API Admin Permissions for the Project sprint link module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/2/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/sprint/", {}, 404, "GET"),

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
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                404,
                "POST",
            ),
            # Both dates are required
            self.URLTest(
                "/api/v1/project/1/sprint/",
                {
                    "title": "API Sprint",
                },
                400,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/sprint/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/2/sprint/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/3/sprint/1/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/project/1/sprint/2/", {}, 400, "DELETE"),
            self.URLTest("/api/v1/project/2/sprint/1/", {}, 400, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_project_user_list(self):
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
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/2/users/",
                {
                    "user_list": [2, 3],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/project/3/users/",
                {
                    "user_list": [2, 3],
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/project/1/users/1/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/2/users/2/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/project/3/users/1/",
                {},
                404,
                "DELETE",
            ),
            # User 5 is only on project 2
            self.URLTest(
                "/api/v1/project/1/users/5/",
                {},
                400,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

