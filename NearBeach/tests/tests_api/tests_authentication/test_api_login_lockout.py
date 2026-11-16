from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework.throttling import SimpleRateThrottle
from unittest.mock import patch

LOGIN_URL = "/api/v1/authentication/"
USERNAME = "team_member"
PASSWORD = "Test1234$"
LOCKOUT_LIMIT = 3

# The test runner switches axes off (see local/settings.py) - these tests switch it back on
LOCKOUT_SETTINGS = {
    "AXES_ENABLED": True,
    "AXES_FAILURE_LIMIT": LOCKOUT_LIMIT,
    "AXES_RESET_ON_SUCCESS": True,
}


@override_settings(**LOCKOUT_SETTINGS)
class ApiAuthenticationLockoutTests(APITestCase):
    """Account lockout after repeated failed logins (django-axes)

    Deliberately not BaseApiClass: the auth throttles are loosened here so only axes can respond 429.
    """

    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        patcher = patch.dict(
            SimpleRateThrottle.THROTTLE_RATES,
            {"auth_minute": "1000/min", "auth_hour": "1000/hour"},
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def _login(self, password="wrong", username=USERNAME, **extra):
        return self.client.post(
            LOGIN_URL,
            {"username": username, "password": password, "otp_token": ""},
            format="json",
            **extra,
        )

    def test_failures_below_limit_are_unauthorised(self):
        for _ in range(LOCKOUT_LIMIT - 1):
            self.assertEqual(self._login().status_code, 401)

    def test_locks_out_after_limit(self):
        for _ in range(LOCKOUT_LIMIT):
            self._login()

        response = self._login()
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json(), {"status": "locked_out"})

    def test_correct_password_rejected_while_locked(self):
        for _ in range(LOCKOUT_LIMIT):
            self._login()

        self.assertEqual(self._login(password=PASSWORD).status_code, 429)

    def test_success_resets_failure_count(self):
        for _ in range(LOCKOUT_LIMIT - 1):
            self._login()
        self.assertEqual(self._login(password=PASSWORD).status_code, 200)

        # Counter reset - the same number of failures doesn't lock the account
        self.client.logout()
        for _ in range(LOCKOUT_LIMIT - 1):
            self.assertEqual(self._login().status_code, 401)

    def test_other_username_not_locked(self):
        for _ in range(LOCKOUT_LIMIT):
            self._login()

        self.assertEqual(self._login(username="team_leader").status_code, 401)

    def test_same_username_other_ip_not_locked(self):
        for _ in range(LOCKOUT_LIMIT):
            self._login(REMOTE_ADDR="10.0.0.1")

        self.assertEqual(self._login(REMOTE_ADDR="10.0.0.2").status_code, 401)
        self.assertEqual(self._login(REMOTE_ADDR="10.0.0.1").status_code, 429)

    def test_unknown_username_locks_with_same_response(self):
        # Must look identical to a real account, otherwise lockout reveals which usernames exist
        for _ in range(LOCKOUT_LIMIT):
            self._login(username="does_not_exist")

        response = self._login(username="does_not_exist")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json(), {"status": "locked_out"})
