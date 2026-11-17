from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoLogInPermissionTests(BaseApiClass):
    def test_api_permissions_no_log_in_task(self):
        """Test - API Not logged-in users for Task"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/6/", {}, 403, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/task/1/",
                {
                    "title": "New API Task Title",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/",
                {
                    "title": "New API Task Title",
                },
                403,
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
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/task/",
                {
                    "title": "API Task",
                    "group_list": [3],
                },
                403,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/", {}, 403, "DELETE"),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/task/6/",
                {
                    "title": "New API Task Title",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/9999/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
        

    def test_api_permissions_no_log_in_task_customers(self):
        """Test - API Admin Permissions for the Task customers submodule"""
        data_list = [
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/customer/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),

            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/customer/", {}, 403, "GET"),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/1/customer/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/customer/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/customer/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_documentation(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/documents/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/documents/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/documents/", {}, 403, "GET"),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/",
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
                "/api/v1/task/1/documents/7/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/7/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
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
                "/api/v1/task/1/documents/7/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5f9d5dc0-a0fb-42ee-bc8e-59edad5afca9/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/7b2b1fca-8a6b-42c9-a421-6c1741641769/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/5/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/dc1dbc09-ec55-4d30-815c-beb0fb990835/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/a6e39cd5-d45d-4c49-a9f4-0f68bc8daa4d/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/dc1dbc09-ec55-4d30-815c-beb0fb990835/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/5f9d5dc0-a0fb-42ee-bc8e-59edad5afca9/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7b2b1fca-8a6b-42c9-a421-6c1741641769/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/1/documents/a6e39cd5-d45d-4c49-a9f4-0f68bc8daa4d/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/documents/7/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/7/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/documents/10/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_groups(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/groups/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/groups/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/groups/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/groups/",
                {
                    "group_list": [1],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/groups/",
                {
                    "group_list": [1],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/groups/",
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
                "/api/v1/task/1/groups/1/",
                {},
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/2/groups/1/",
                {},
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/task/3/groups/1/",
                {},
                403,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_links(self):
        """Test - API Admin Permissions for the Task Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/link_list/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/link_list/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/link_list/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/link_list/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/link_list/",
                {
                    "object_type": "project",
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
                "/api/v1/task/1/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/48/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/link_list/48/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/link_list/43/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/link_list/43/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/link_list/48/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/link_list/43/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/1/link_list/48/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/link_list/43/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_notes(self):
        """Test - API Admin Permissions for the Task Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/notes/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/notes/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/notes/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/notes/",
                {
                    "note": "Hello World",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/",
                {
                    "note": "Hello World",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/notes/",
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
                "/api/v1/task/1/notes/5/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/8/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/notes/8/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/notes/5/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/notes/5/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/notes/8/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/1/notes/8/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/notes/5/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_organisation(self):
        """Test - API Admin Permissions for the Task organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/organisation/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/organisation/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/organisation/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/organisation/",
                {
                    "id": 1,
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/organisation/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/organisation/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/organisation/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_public_link(self):
        """Test - API Admin Permissions for the Task public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/task/1/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/2/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/task/3/public_link/", {}, 403, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/task/1/public_link/",
                {},
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/",
                {},
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/public_link/",
                {},
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/3/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/1/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/task/2/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/1/public_link/c5994697-a7e6-4e54-b8b1-4dee7315d7ea/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/public_link/1c1067e9-563f-4419-9dac-e87d757ecb37/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_log_in_task_user_list(self):
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
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/2/users/",
                {
                    "user_list": [2, 3],
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/task/3/users/",
                {
                    "user_list": [2, 3],
                },
                403,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/task/1/users/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/2/users/2/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/3/users/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/task/1/users/5/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
