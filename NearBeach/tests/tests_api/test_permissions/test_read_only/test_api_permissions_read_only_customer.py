from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiReadOnlyPermissionTests(BaseApiClass):
    username = "read_only"
    password = "Test1234$"

    def test_api_permissions_read_only_customers(self):
        """Test - API ReadOnly Permissions for the customers of an Organisation"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/1/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 404, "GET"),
            self.URLTest("/api/v1/organisation/2/customer/", {}, 404, "GET"),
            #########
            # UPDATE
            #########
            self.URLTest(
                "/api/v1/organisation/1/customer/1/",
                {
                    'first_name': 'Changed'
                },
                403,
                "PATCH"
            ),
            self.URLTest(
                "/api/v1/organisation/2/customer/1/",
                {
                    'first_name': 'Changed'
                },
                404,
                "PATCH"
            ),
            #########
            # CREATE
            #########
            self.URLTest(
                "/api/v1/organisation/1/customer/",
                {
                    'first_name': 'Api',
                    'last_name': 'Customer',
                    'email': 'api.customer@api.example',
                    'title': 1
                },
                403,
                "POST"
            ),
            self.URLTest(
                "/api/v1/organisation/2/customer/",
                {
                    'first_name': 'Api',
                    'last_name': 'Customer',
                    'email': 'api.customer@api.example',
                    'title': 1
                },
                404,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)
