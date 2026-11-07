from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiReadOnlyPermissionTests(BaseApiClass):
    username = "read_only"
    password = "Test1234$"

    def test_api_permissions_read_only_organisation(self):
        """Test - API ReadOnly Permissions for the Organisation module"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/", {}, 200, "GET"),
            #########
            # READ
            #########
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
