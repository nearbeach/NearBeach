from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoLogInPermissionTests(BaseApiClass):
    """Not logged-in users - every organisation and customer endpoint is refused"""

    def test_api_permissions_no_log_in_customers(self):
        """Test - API NoLogIn Permissions for the customers of an Organisation"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/customer/", {}, 403, "GET"),
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
                403,
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
                403,
                "POST"
            ),
            #########
            # DELETE
            #########
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)
