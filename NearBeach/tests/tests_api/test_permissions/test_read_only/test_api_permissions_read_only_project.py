from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiReadOnlyPermissionTests(BaseApiClass):
    username = "read_only"
    password = "Test1234$"

    def test_api_permissions_read_only_project(self):
        """Test - API Read Only Permissions for Project (exclude delete)"""
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
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)