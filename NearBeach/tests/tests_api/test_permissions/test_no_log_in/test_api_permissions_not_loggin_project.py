from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoLogInPermissionTests(BaseApiClass):
    def test_api_permissions_no_log_in_project(self):
        """Test - API Not logged-in users for Project"""
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
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
