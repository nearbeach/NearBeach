from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiForgottenPasswordTests(BaseApiClass):
    def test_password_reset_with_user(self):
        """Test - API Forgotten password with existing user"""
        data_list = [
            ######################
            # FORGOTTEN PASSWORD
            ######################
            self.URLTest(
                "/api/v1/authentication/forgotten-password/",
                {
                    "email": "support@nearbeach.org",
                },
                200,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_password_reset_with_non_existing_user(self):
        """Test - API Forgotten password with existing user"""
        data_list = [
            ######################
            # FORGOTTEN PASSWORD
            ######################
            self.URLTest(
                "/api/v1/authentication/forgotten-password/",
                {
                    "email": "non-existing-user@nearbeach.org",
                },
                200,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_password_reset_with_incorrect_form(self):
        """Test - API Forgotten password with existing user"""
        data_list = [
            ######################
            # FORGOTTEN PASSWORD
            ######################
            self.URLTest(
                "/api/v1/authentication/forgotten-password/",
                {
                    "emails": "non-existing-user@nearbeach.org",
                },
                400,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/forgotten-password/",
                {},
                400,
                "POST",
            ),
        ]

        self._run_test_array(data_list)
