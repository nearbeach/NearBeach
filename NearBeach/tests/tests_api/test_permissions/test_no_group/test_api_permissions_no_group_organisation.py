from django.contrib.auth.models import User

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoGroupPermissionTests(BaseApiClass):
    username = "no_group"
    password = "Test1234$"

    # OVERRIDE - a user in no group can not log in through the api, but can still hold a session
    def _login_user(self):
        self.client.force_login(User.objects.get(username=self.username))

    def test_api_permissions_no_group_organisation(self):
        """Test - API NoGroup Permissions for the Organisation module"""
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
