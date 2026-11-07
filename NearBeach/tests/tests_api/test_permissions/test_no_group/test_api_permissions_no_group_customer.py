from django.contrib.auth.models import User

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoGroupPermissionTests(BaseApiClass):
    username = "no_group"
    password = "Test1234$"

    # OVERRIDE - a user in no group can not log in through the api, but can still hold a session
    def _login_user(self):
        self.client.force_login(User.objects.get(username=self.username))

    def test_api_permissions_no_group_customers(self):
        """Test - API NoGroup Permissions for the customers of an Organisation"""
        data_list = [
            #########
            # READ
            #########
            self.URLTest("/api/v1/organisation/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "GET"),
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
