from unittest.mock import patch

from django.core.cache import cache
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.throttling import SimpleRateThrottle
import time

LOGIN_URL = "/api/v1/authentication/"
FORGOTTEN_URL = "/api/v1/authentication/forgotten-password/"
RESET_URL = "/api/v1/authentication/reset-password/"
USERNAME = "team_member"
PASSWORD = "Test1234$"


class ApiAuthenticationThrottlingTests(APITestCase):
    """Brute-force protection on the authentication endpoints.

    Notes
    ~~~~~
    - Deliberately does NOT use BaseApiClass: that class switches the login throttles off
    - Throttle history lives in Django's cache, which survives between tests - so it is cleared
      before and after every test
    - Rates are patched in `SimpleRateThrottle.THROTTLE_RATES`, the dict DRF reads each throttle's rate from
    - Time is controlled through `SimpleRateThrottle.timer` so the tests never sleep
    """

    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.clock = [1_000_000.0]
        self._patch_timer()

    def _patch_timer(self):
        patcher = patch.object(SimpleRateThrottle, "timer", staticmethod(lambda: self.clock[0]))
        patcher.start()
        self.addCleanup(patcher.stop)

    # ---------- helpers ----------
    @staticmethod
    def _rates(minute="1000/min", hour="1000/hour"):
        return patch.dict(
            SimpleRateThrottle.THROTTLE_RATES,
            {"auth_minute": minute, "auth_hour": hour},
        )

    def _login(self, password="wrong", otp_token="", username=USERNAME, **extra):
        return self.client.post(
            LOGIN_URL,
            {"username": username, "password": password, "otp_token": otp_token},
            format="json",
            **extra,
        )

    def _count_until_throttled(self, attempts, **kwargs):
        """Number of requests accepted (not 429) before the first 429"""
        for count in range(attempts):
            if self._login(**kwargs).status_code == 429:
                return count
        return attempts

    # ---------- the throttle works ----------
    def test_repeated_failed_logins_are_eventually_throttled(self):
        with self._rates(minute="10/min"):
            accepted = self._count_until_throttled(30)

        self.assertGreater(accepted, 0, "First attempt should not be throttled")
        self.assertLess(accepted, 30, "Brute force attempts were never throttled")

    def test_throttled_response_has_retry_after(self):
        with self._rates(minute="3/min"):
            self._count_until_throttled(30)
            response = self._login()

        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response.headers)
        self.assertGreater(int(response.headers["Retry-After"]), 0)

    def test_correct_password_is_also_blocked_while_throttled(self):
        """A throttled attacker must not be able to 'win' on the next guess"""
        with self._rates(minute="3/min"):
            self._count_until_throttled(30)
            response = self._login(password=PASSWORD)

        self.assertEqual(response.status_code, 429)
        self.assertEqual(self.client.get("/api/v1/project/").status_code, 403)

    def test_successful_logins_count_towards_the_limit(self):
        with self._rates(minute="3/min"):
            accepted = self._count_until_throttled(30, password=PASSWORD)

        self.assertLess(accepted, 30)

    def test_throttle_is_per_ip_address(self):
        with self._rates(minute="3/min"):
            self._count_until_throttled(30, REMOTE_ADDR="10.0.0.1")
            blocked = self._login(REMOTE_ADDR="10.0.0.1")
            other_ip = self._login(REMOTE_ADDR="10.0.0.2")

        self.assertEqual(blocked.status_code, 429)
        self.assertEqual(other_ip.status_code, 401, "A different IP should not be affected")

    def test_throttle_is_per_ip_not_per_username(self):
        """Known trade-off: one IP guessing many usernames is throttled as a whole"""
        with self._rates(minute="3/min"):
            self._count_until_throttled(30, username="team_member")
            other_user = self._login(username="team_leader")

        self.assertEqual(other_user.status_code, 429)

    def test_login_works_again_after_the_window_passes(self):
        with self._rates(minute="3/min"):
            self._count_until_throttled(30)
            self.assertEqual(self._login().status_code, 429)

            self.clock[0] += 61  # a minute later
            response = self._login(password=PASSWORD)

        self.assertEqual(response.status_code, 200)

    def test_still_throttled_just_before_the_window_passes(self):
        with self._rates(minute="3/min"):
            self._count_until_throttled(30)
            self.clock[0] += 30
            response = self._login()

        self.assertEqual(response.status_code, 429)

    # ---------- two-factor brute force ----------
    def test_wrong_two_factor_codes_are_throttled_and_lock_out_the_real_code(self):
        """6-digit codes are guessable without a limit - the throttle must stop the guessing"""
        user = User.objects.get(username=USERNAME)
        device = TOTPDevice.objects.create(user=user, name="t", confirmed=True)

        with self._rates(minute="5/min"):
            accepted = self._count_until_throttled(30, password=PASSWORD, otp_token="000000")

            totp = TOTP(key=device.bin_key, step=device.step, t0=device.t0, digits=device.digits)
            totp.time = time.time()
            real_code = str(totp.token()).zfill(device.digits)
            response = self._login(password=PASSWORD, otp_token=real_code)

        self.assertLess(accepted, 30, "Two-factor guesses were never throttled")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(self.client.get("/api/v1/project/").status_code, 403)

    # ---------- the other authentication endpoints ----------
    def test_forgotten_password_is_throttled(self):
        statuses = []
        with self._rates(minute="3/min"):
            for _ in range(30):
                statuses.append(
                    self.client.post(
                        FORGOTTEN_URL, {"email": "support@nearbeach.org"}, format="json"
                    ).status_code
                )

        self.assertIn(429, statuses)

    def test_reset_password_is_throttled(self):
        statuses = []
        with self._rates(minute="3/min"):
            for _ in range(30):
                statuses.append(
                    self.client.post(
                        RESET_URL,
                        {"token": "x", "password": "NewPass1234$", "confirm_password": "NewPass1234$"},
                        format="json",
                    ).status_code
                )

        self.assertIn(429, statuses)

    def test_login_and_forgotten_password_share_one_throttle_bucket(self):
        """Documents current behaviour: both endpoints draw from the same per-IP allowance"""
        with self._rates(minute="3/min"):
            self._count_until_throttled(30)
            response = self.client.post(FORGOTTEN_URL, {"email": "support@nearbeach.org"}, format="json")

        self.assertEqual(response.status_code, 429)

    # ---------- configured limits are honoured ----------
    def test_minute_limit_allows_exactly_the_configured_number_of_requests(self):
        """Regression: the minute and hour throttles once shared a scope (and so a cache key),
        recording each request twice - a '6/min' limit only allowed 3 requests."""
        with self._rates(minute="6/min"):
            accepted = self._count_until_throttled(30)

        self.assertEqual(accepted, 6)

    def test_hourly_limit_is_enforced(self):
        """Regression: AuthHourThrottle once used scope 'auth_minute', so THROTTLE_AUTH_HOUR was never applied."""
        with self._rates(minute="1000/min", hour="4/hour"):
            accepted = self._count_until_throttled(30)

        self.assertEqual(accepted, 4)
