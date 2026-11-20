from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.tests.utils.RequirementRelatedFixtures import RequirementRelatedFixtures


class ApiAdminPermissionTests(RequirementRelatedFixtures, BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_requirement_item(self):
        """Test - API Admin Permissions for the RequirementItem module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/2/requirement_item/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/1/requirement_item/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/",
                {
                    "title": "New API RequirementItem Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/",
                {
                    "title": "New API RequirementItem Title",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/",
                {
                    "title": "New API RequirementItem Title",
                },
                404,
                "PATCH",
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                    "group_list": [1],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                    "group_list": [2],
                },
                201,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                    "group_list": [3],
                },
                400,
                "POST"
            ),
            # Missing group_list must be a 400, not a 500
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                },
                400,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/", {}, 204, "DELETE"),
            # The create tests above have made requirement_items 3+, so use an id that is never reached
            self.URLTest("/api/v1/requirement/3/requirement_item/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_item_documentation(self):
        """Test - API Admin Permissions for the RequirementItem Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/documents/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/documents/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/",
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
                "/api/v1/requirement/1/requirement_item/1/documents/2001/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2002/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/2001/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/2002/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
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
                "/api/v1/requirement/1/requirement_item/1/documents/2001/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000001/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000002/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/2002/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000003/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2002/",
                {
                    "type": "folder",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000003/",
                {
                    "type": "link",
                },
                204,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000001/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000002/",
                {
                    "type": "document",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/2001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/10/",
                {
                    "type": "folder",
                },
                404,
                "DELETE"
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_item_links(self):
        """Test - API Admin Permissions for the RequirementItem Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/link_list/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/",
                {
                    "object_type": "requirement_item",
                    "object_id": "2",
                    "object_relation": "relates",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/link_list/",
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
                "/api/v1/requirement/1/requirement_item/1/link_list/9001/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9003/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/link_list/9001/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/link_list/9003/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9001/",
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
                "/api/v1/requirement/1/requirement_item/1/link_list/9001/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9003/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/link_list/9001/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/link_list/9003/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9001/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_item_notes(self):
        """Test - API Admin Permissions for the RequirementItem Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/notes/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/notes/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/",
                {
                    "note": "Hello World",
                },
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/notes/",
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
                "/api/v1/requirement/1/requirement_item/1/notes/12/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/13/",
                {
                    "note": "Hello World",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/notes/13/",
                {
                    "note": "Hello World",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/12/",
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
                "/api/v1/requirement/1/requirement_item/1/notes/12/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/13/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/notes/13/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/12/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_admin_requirement_item_public_link(self):
        """Test - API Admin Permissions for the RequirementItem public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/public_link/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/",
                {},
                201,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/public_link/",
                {},
                404,
                "POST",
            ),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/",
                {
                    "is_active": "false",
                },
                200,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/",
                {
                    "is_active": "false",
                },
                404,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
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
                "/api/v1/requirement/1/requirement_item/1/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/",
                {},
                204,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/",
                {},
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {},
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_requirement_item_must_belong_to_the_requirement_in_the_url(self):
        """Test - an item is only reachable through its own requirement

        The permission check reads the requirement in the url, so the item has to be matched to it too. Item 1
        belongs to requirement 1 (Administration) and item 2 to requirement 2 (QA Team); item 99999 does not exist.
        Anyone who can reach the requirement gets a 404, anyone who cannot gets a 403."""
        data_list = [
            self.URLTest("/api/v1/requirement/2/requirement_item/1/notes/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/1/public_link/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/1/link_list/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/1/documents/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/1/notes/", {"note": "Hello World"}, 404, "POST"),
            self.URLTest("/api/v1/requirement/2/requirement_item/99999/notes/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/99999/", {"title": "New API RequirementItem Title"}, 404, "PATCH"),
            self.URLTest("/api/v1/requirement/1/requirement_item/2/notes/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)
