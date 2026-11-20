from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.tests.utils.RequirementRelatedFixtures import RequirementRelatedFixtures


class ApiAdminPermissionTests(RequirementRelatedFixtures, BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_requirement(self):
        """Test - API Admin Permissions for the Requirement module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/",
                {
                    "title": "New API Requirement Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/",
                {
                    "title": "New API Requirement Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/",
                {
                    "title": "New API Requirement Title",
                },
                404,
                "PATCH",
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/",
                {
                    "title": "API Requirement",
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/",
                {
                    "title": "API Requirement",
                    "group_list": [1],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/",
                {
                    "title": "API Requirement",
                    "group_list": [2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/",
                {
                    "title": "API Requirement",
                    "group_list": [3],
                },
                400,
                "POST"
            ),
            # Missing group_list must be a 400, not a 500
            self.URLTest(
                "/api/v1/requirement/",
                {
                    "title": "API Requirement",
                },
                400,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/2/", {}, 204, "DELETE"),
            # The create tests above have made requirements 3+, so use an id that is never reached
            self.URLTest("/api/v1/requirement/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_customers(self):
        """Test - API Admin Permissions for the Requirement customers submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/customer/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/customer/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/customer/",
                {
                    "id": 1,
                },
                404,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/1/customer/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/2/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/2/customer/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/3/customer/1/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/3/customer/2/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_documentation(self):
        """Test - API Admin Permissions for the Requirement Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/documents/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/documents/",
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
                "/api/v1/requirement/1/documents/1001/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/1002/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/documents/1001/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/1002/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/1001/",
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
                "/api/v1/requirement/1/documents/1001/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/00000000-aaaa-4000-8000-000000000001/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/00000000-aaaa-4000-8000-000000000002/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/1002/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/00000000-aaaa-4000-8000-000000000003/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/00000000-aaaa-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/1002/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/1001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/00000000-aaaa-4000-8000-000000000003/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/00000000-aaaa-4000-8000-000000000001/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/00000000-aaaa-4000-8000-000000000002/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/documents/00000000-aaaa-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/documents/1001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/3/documents/1001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/3/documents/10/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_groups(self):
        """Test - API Admin Permissions for the Requirement Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/groups/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/groups/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/groups/",
                {
                    "group_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/groups/",
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
                "/api/v1/requirement/1/groups/1/",
                {},
                400, # Cannot remove last group from requirement
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/groups/1/",
                {},
                200,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/groups/1/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_links(self):
        """Test - API Admin Permissions for the Requirement Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/link_list/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "2",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/link_list/",
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
                "/api/v1/requirement/1/link_list/55/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/link_list/56/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/link_list/55/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/link_list/46/",
                {
                    "object_type": "task",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/link_list/55/",
                {
                    "object_type": "task",
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
                "/api/v1/requirement/1/link_list/55/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/link_list/56/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/link_list/55/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/link_list/46/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/link_list/55/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_notes(self):
        """Test - API Admin Permissions for the Requirement Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/notes/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/notes/",
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
                "/api/v1/requirement/1/notes/4/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/notes/11/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/notes/11/",
                {
                    "note": "Hello World",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/notes/4/",
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
                "/api/v1/requirement/1/notes/4/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/notes/11/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/notes/11/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/notes/4/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_organisation(self):
        """Test - API Admin Permissions for the Requirement organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/organisation/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/organisation/",
                {
                    "id": 1,
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/organisation/",
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
                "/api/v1/requirement/1/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/organisation/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/organisation/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/organisation/2/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/organisation/4/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_public_link(self):
        """Test - API Admin Permissions for the Requirement public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/public_link/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/public_link/",
                {},
                404,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/public_link/5435086c-a145-4540-bc71-35a0fd0ee171/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/public_link/5435086c-a145-4540-bc71-35a0fd0ee171/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
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
                "/api/v1/requirement/1/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/public_link/5435086c-a145-4540-bc71-35a0fd0ee171/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/public_link/5435086c-a145-4540-bc71-35a0fd0ee171/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/public_link/fbda2f94-be7b-41e5-b93a-3ce65516d09d/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_sprint_links(self):
        """Test - API Admin Permissions for the Requirement sprint link module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/sprint/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/sprint/",
                {
                    "title": "API Sprint",
                    "start_date": "2026-01-05",
                    "end_date": "2026-01-12",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/sprint/",
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
                "/api/v1/requirement/1/sprint/",
                {
                    "title": "API Sprint",
                },
                400,
                "POST",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/sprint/3/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/2/sprint/4/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/3/sprint/3/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/1/sprint/4/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/2/sprint/3/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_user_list(self):
        """Test - API Admin Permissions for the Requirement user list module"""
        data_list = [
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/users/",
                {
                    "user_list": [1],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/users/",
                {
                    "user_list": [2, 3],
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/users/",
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
                "/api/v1/requirement/1/users/1/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/users/2/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/users/1/",
                {},
                404,
                "DELETE",
            ),
            # User 5 is only on requirement 2
            self.URLTest(
                "/api/v1/requirement/1/users/5/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)


    def test_api_permissions_admin_requirement_audit(self):
        """Test - the audit history follows the same read permission as the requirement itself"""
        data_list = [
            self.URLTest("/api/v1/requirement/1/audit/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/audit/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/audit/", {}, 404, "GET"),
        ]
        self._run_test_array(data_list)
