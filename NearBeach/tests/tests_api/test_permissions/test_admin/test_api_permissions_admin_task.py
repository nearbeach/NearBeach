from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAdminPermissionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_task(self):
        """Test - API Admin Permissions for the Task module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/task/1/",
                {
                    "title": "New API Task Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/",
                {
                    "title": "New API Task Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/",
                {
                    "title": "New API Task Title",
                },
                404,
                "PATCH",
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                    "group_list": [1],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                    "group_list": [2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                    "group_list": [3],
                },
                400,
                "POST"
            ),
            # Missing group_list must be a 400, not a 500
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                },
                400,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/task/2/", {}, 204, "DELETE"),
            # The create tests above have made tasks 3+, so use an id that is never reached
            self.URLTest("/api/v1/task/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_customers(self):
        """Test - API Admin Permissions for the Task customers submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/customer/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/customer/",
                {
                    "id": 1,
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/task/1/customer/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/task/2/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/task/2/customer/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/task/3/customer/1/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/task/3/customer/2/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_documentation(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/documents/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/",
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
                "/api/v1/task/1/documents/7/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/7/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            # NOTE - we only need to test the folder, as this is a permission check only. Links and Uploads hit the
            # same endpoint. Thus they are not here

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/task/1/documents/7/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5f9d5dc0-a0fb-42ee-bc8e-59edad5afca9/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/7b2b1fca-8a6b-42c9-a421-6c1741641769/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/dc1dbc09-ec55-4d30-815c-beb0fb990835/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/a6e39cd5-d45d-4c49-a9f4-0f68bc8daa4d/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/dc1dbc09-ec55-4d30-815c-beb0fb990835/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5f9d5dc0-a0fb-42ee-bc8e-59edad5afca9/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7b2b1fca-8a6b-42c9-a421-6c1741641769/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/1/documents/a6e39cd5-d45d-4c49-a9f4-0f68bc8daa4d/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/3/documents/7/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/task/3/documents/10/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_groups(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/groups/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/groups/",
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
                "/api/v1/task/1/groups/1/",
                {},
                400, # Cannot remove last group from task
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/groups/1/",
                {},
                200,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/groups/1/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_links(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/link_list/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "2",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/link_list/",
                {
                    "object_type": "project",
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
                "/api/v1/task/1/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/48/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/link_list/48/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/task/1/link_list/43/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/48/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/link_list/43/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/link_list/48/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/43/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_notes(self):
        """Test - API Admin Permissions for the Task Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/notes/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/notes/",
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
                "/api/v1/task/1/notes/5/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/8/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/notes/8/",
                {
                    "note": "Hello World",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/5/",
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
                "/api/v1/task/1/notes/5/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/8/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/notes/8/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/5/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_organisation(self):
        """Test - API Admin Permissions for the Task organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/organisation/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/organisation/",
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
                "/api/v1/task/1/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/organisation/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/organisation/2/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/organisation/4/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_public_link(self):
        """Test - API Admin Permissions for the Task public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/task/3/public_link/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/public_link/",
                {},
                404,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/task/1/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest(
                "/api/v1/task/1/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_task_user_list(self):
        """Test - API Admin Permissions for the Task user list module"""
        data_list = [
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/users/",
                {
                    "user_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/users/",
                {
                    "user_list": [2, 3],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/users/",
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
                "/api/v1/task/1/users/1/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/users/2/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/users/1/",
                {},
                404,
                "DELETE",
            ),
            # User 5 is only on task 2
            self.URLTest(
                "/api/v1/task/1/users/5/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)
