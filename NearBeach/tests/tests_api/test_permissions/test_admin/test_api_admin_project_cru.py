from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAdminPermissionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_project_data(self):
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

            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/project/",
                {
                    "name": "API Project",
                    "group_list": [1, 2],
                },
                201,
                "POST"
            ),
        ]

        self._run_test_array(data_list)