from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiTeamMemberPermissionTests(BaseApiClass):
    username = "team_member"
    password = "Test1234$"

    def test_api_permissions_team_member_project(self):
        """Test - API Team Member Permissions for Project"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/6/", {}, 404, "GET"),
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
                200,
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
                400,
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
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_customers(self):
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
            # TODO - Create fixture where these are already assigned
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_documentation(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/documents/", {}, 403, "GET"),
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
                403,
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
            #########
            # UPDATE
            #########
            # TODO - Implement update functionality for renaming folders/documents/links etc

            #########
            # DELETE
            #########
            # TODO - Insert folders/documents/links etc into fixture so we can test this
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_groups(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/groups/", {}, 403, "GET"),
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
                403,
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
                403,
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

    def test_api_permissions_team_member_project_links(self):
        """Test - API Admin Permissions for the Project Documentation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/link_list/", {}, 403, "GET"),
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
            # DELETE
            #########
            # TODO - Create links in the fixture so we can test deleting them
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_misc(self):
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

    def test_api_permissions_team_member_project_notes(self):
        """Test - API Admin Permissions for the Project Notes submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/notes/", {}, 403, "GET"),
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
                403,
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
            # TODO - Add in notes into the fixture and write tests against this

            #########
            # DELETE
            #########
            # TODO - Add in notes into the fixture and write tests against this
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_organisation(self):
        """Test - API Admin Permissions for the Project organisation submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/organisation/", {}, 403, "GET"),
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
                403,
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
            # TODO - Create fixture where these are already assigned
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_public_link(self):
        """Test - API Admin Permissions for the Project public links submodule"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/public_link/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/public_link/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/public_link/", {}, 404, "GET"),

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
            # TODO - Create fixture where it contains public links

            #########
            # DELETE
            #########
            # TODO - Create fixture where it contains public links
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_sprint_links(self):
        """Test - API Admin Permissions for the Project sprint link module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/1/sprint/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/sprint/", {}, 200, "GET"),
            self.URLTest("/api/v1/project/3/sprint/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_member_project_user_list(self):
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
            # TODO - Update fixture to have some projects with assigned users to remove etc.
        ]

        self._run_test_array(data_list)
    