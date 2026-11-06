from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAdminPermissionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_api_permissions_admin_organisation(self):
        """Test - API Admin Permissions for reading an Organisation"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/2/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/organisation/1/",
                {
                    'name': 'New API Organisation Name'
                },
                200,
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
                201,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/organisation/2/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/organisation/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/organisation/9999/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)
