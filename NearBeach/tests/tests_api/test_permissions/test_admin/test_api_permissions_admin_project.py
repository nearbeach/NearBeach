from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAdminPermissionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_project(self):
        """Test - API Admin Permissions for Project (exclude delete)"""
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
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/project/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/project/2/", {}, 204, "DELETE"),
        ]

        self._run_test_array(data_list)