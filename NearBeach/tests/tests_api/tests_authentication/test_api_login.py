# TODO - Test two factor authentication (how? Look this up)

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAuthenticationLoginTests(BaseApiClass):
    def test_successful_logins(self):
        """Test - API Authentication successfully logs everyone in"""
        data_list = [
            #########
            # LOGIN
            #########
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "admin",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                200,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_leader",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                200,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_member",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                200,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_intern",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                200,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "read_only",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                200,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_incorrect_password_logins(self):
        """Test - API Authentication by using wrong password"""
        data_list = [
            #########
            # LOGIN
            #########
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "admin",
                    "password": "Test1234",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_leader",
                    "password": "Test1234",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_member",
                    "password": "Test1234",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "team_intern",
                    "password": "Test1234",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "read_only",
                    "password": "Test1234",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_no_permission_logins(self):
        """Test - API Authentication by using a user with no groups associated with them"""
        data_list = [
            #########
            # LOGIN
            #########
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "no_group",
                    "password": "Test1234$",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_non_existing_logins(self):
        """Test - API Authentication by using a made up user"""
        data_list = [
            #########
            # LOGIN
            #########
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "non_existing_user",
                    "password": "with_made_up_password",
                    "otp_token": "",
                },
                401,
                "POST",
            ),
        ]

        self._run_test_array(data_list)

    def test_incorrect_form_data_logins(self):
        """Test - API Authentication by using incorrect form submission"""
        data_list = [
            #########
            # LOGIN
            #########
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "password": "Test1234$",
                    "otp_token": "",
                },
                400,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "admin",
                    "otp_token": "",
                },
                400,
                "POST",
            ),
            self.URLTest(
                "/api/v1/authentication/",
                {
                    "username": "admin",
                    "password": "Test1234$",
                },
                400,
                "POST",
            ),
        ]

        self._run_test_array(data_list)
