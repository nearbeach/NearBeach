from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.tests.utils.RequirementRelatedFixtures import RequirementRelatedFixtures


class ApiReadOnlyPermissionTests(RequirementRelatedFixtures, BaseApiClass):
    username = "read_only"
    password = "Test1234$"

    def test_api_permissions_read_only_requirement_item(self):
        """Test - API Read Only Permissions for RequirementItem (exclude delete)"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/2/requirement_item/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/1/requirement_item/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/6/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/",
                {
                    "title": "New API RequirementItem Title",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/",
                {
                    "title": "New API RequirementItem Title",
                },
                403,
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
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/",
                {
                    "title": "API RequirementItem",
                    "group_list": [3],
                },
                403,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/", {}, 403, "DELETE"),

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/6/",
                {
                    "title": "New API RequirementItem Title",
                },
                404,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/3/requirement_item/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_read_only_requirement_item_documentation(self):
        """Test - API Admin Permissions for the RequirementItem Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/documents/", {}, 403, "GET"),
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
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/",
                {
                    "description": "Creating Folder",
                    "type": "folder",
                },
                403,
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

            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/2001/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2002/",
                {
                    "description": "Rename Folder",
                    "type": "folder",
                },
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
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
                "/api/v1/requirement/1/requirement_item/1/documents/2001/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000001/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000002/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/2002/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000003/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2002/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000003/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000001/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/00000000-bbbb-4000-8000-000000000002/",
                {
                    "type": "document",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/documents/00000000-bbbb-4000-8000-000000000004/",
                {
                    "type": "link",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/documents/2001/",
                {
                    "type": "folder",
                },
                403,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/2001/",
                {
                    "type": "folder",
                },
                404,
                "DELETE",
            ),
            self.URLTest(
                "/api/v1/requirement/3/requirement_item/3/documents/10/",
                {
                    "type": "folder",
                },
                404,
                "DELETE",
            ),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_read_only_requirement_item_links(self):
        """Test - API Admin Permissions for the RequirementItem Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/link_list/", {}, 403, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/link_list/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/link_list/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/link_list/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "relates",
                },
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9003/",
                {
                    "object_type": "project",
                    "object_id": "1",
                    "object_relation": "blocking",
                },
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/link_list/9001/",
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
            self.URLTest("/api/v1/requirement/1/requirement_item/1/link_list/9001/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/link_list/9003/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/link_list/9001/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/1/requirement_item/1/link_list/9003/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/link_list/9001/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_read_only_requirement_item_notes(self):
        """Test - API Admin Permissions for the RequirementItem Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/notes/", {}, 403, "GET"),
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
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/",
                {
                    "note": "Hello World",
                },
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/13/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/notes/13/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/notes/12/",
                {
                    "note": "Hello World",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/notes/12/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/notes/13/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/1/requirement_item/1/notes/13/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/notes/12/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_read_only_requirement_item_public_link(self):
        """Test - API Admin Permissions for the RequirementItem public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/public_link/", {}, 404, "GET"),

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/requirement/1/requirement_item/1/public_link/",
                {},
                403,
                "POST",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/",
                {},
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/",
                {
                    "is_active": "false",
                },
                403,
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
                403,
                "PATCH",
            ),
            self.URLTest(
                "/api/v1/requirement/2/requirement_item/2/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/",
                {
                    "is_active": "false",
                },
                403,
                "PATCH",
            ),

            #########
            # DELETE
            #########
            self.URLTest("/api/v1/requirement/1/requirement_item/1/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/3/requirement_item/3/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/requirement/1/requirement_item/1/public_link/9b6a9317-df46-453f-aa5b-6f33b77c28c4/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/requirement/2/requirement_item/2/public_link/aba74809-aae5-4fc4-8929-5fd835fefa22/", {}, 403, "DELETE"),
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
            self.URLTest("/api/v1/requirement/2/requirement_item/1/notes/", {"note": "Hello World"}, 403, "POST"),
            self.URLTest("/api/v1/requirement/2/requirement_item/99999/notes/", {}, 404, "GET"),
            self.URLTest("/api/v1/requirement/2/requirement_item/99999/", {"title": "New API RequirementItem Title"}, 403, "PATCH"),
            self.URLTest("/api/v1/requirement/1/requirement_item/2/notes/", {}, 403, "GET"),
        ]

        self._run_test_array(data_list)
