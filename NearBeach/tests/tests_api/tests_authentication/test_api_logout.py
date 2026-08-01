from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiAuthenticationLogoutTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_successful_logout(self):
        """Test - API Authentication successfully logout"""
        data_list = [
            #########
            # LOGOUT
            #########
            self.URLTest(
                "/logout/",
                {},
                302,
                "GET",
            ),
        ]

        self._run_test_array(data_list)