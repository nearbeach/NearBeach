from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoPermissionPermissionTests(BaseApiClass):
    username = "team_no_permissions"
    password = "Test1234$"

    def test_api_permissions_no_permission_organisation(self):
        """Test - API NoPermission Permissions for the Organisation module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/", {}, 403, "GET"),
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/organisation/1/",
                {
                    'name': 'New API Organisation Name'
                },
                403,
                "PATCH"
            ),
            self.URLTest(
                "/api/v1/organisation/2/",
                {
                    'name': 'New API Organisation Name'
                },
                404,
                "PATCH"
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/organisation/",
                {
                    'name': 'API Organisation',
                    'website': 'https://api.example',
                    'email': 'api@api.example'
                },
                403,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/organisation/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/organisation/1/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
