from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoGroupPermissionTests(BaseApiClass):
    username = "no_group"
    password = "Test1234$"

    def test_api_permissions_no_group_project(self):
        """Test - API No Group Permissions for Project"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/project/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/project/2/", {}, 403, "GET"),
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
