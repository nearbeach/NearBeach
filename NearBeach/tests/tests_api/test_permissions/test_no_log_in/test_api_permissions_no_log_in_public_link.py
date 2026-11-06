from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoLogInPublicLinkPermissionTests(BaseApiClass):
    """Not logged-in users - the public link api still needs a log in"""

    def test_api_permissions_no_log_in_public_link(self):
        """Test - API NoLogIn Permissions for the Public Link module"""
        data_list = [
            self.URLTest("/api/v1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 403, "GET"),
            self.URLTest("/api/v1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/", {}, 403, "GET"),
            self.URLTest("/api/v1/public_link/00000000-0000-0000-0000-000000000000/", {}, 403, "GET"),
            self.URLTest("/api/v1/public_link/not-a-uuid/", {}, 403, "GET"),
        ]

        self._run_test_array(data_list)
