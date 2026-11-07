import base64
import time
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, override_settings
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.test import APIClient, APITestCase
from rest_framework.throttling import SimpleRateThrottle

LOGIN_URL = "/api/v1/authentication/"
API_URL = "/api/v1/user/initial_data/"
ADMIN_LOGIN_URL = "/admin/login/"
USERNAME = "team_member"
PASSWORD = "Test1234$"


def basic(username=USERNAME, password=PASSWORD):
    return "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()


def totp_token(device):
    totp = TOTP(key=device.bin_key, step=device.step, t0=device.t0, digits=device.digits)
    totp.time = time.time()
    return str(totp.token()).zfill(device.digits)


class LoginHardeningTestBase(APITestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)

    def _rates(self, minute="1000/min", hour="1000/hour"):
        patcher = patch.dict(SimpleRateThrottle.THROTTLE_RATES, {"auth_minute": minute, "auth_hour": hour})
        patcher.start()
        self.addCleanup(patcher.stop)

    @staticmethod
    def _add_two_factor(username=USERNAME):
        return TOTPDevice.objects.create(user=User.objects.get(username=username), name="phone", confirmed=True)


class BasicAuthenticationTests(LoginHardeningTestBase):
    """HTTP Basic is a password-only way into the API, so it must not be a way around two-factor authentication"""

    def _get(self, header):
        return APIClient().get(API_URL, HTTP_AUTHORIZATION=header)

    def test_a_user_without_two_factor_can_still_use_basic(self):
        self.assertEqual(self._get(basic()).status_code, 200)

    def test_a_user_with_two_factor_is_refused(self):
        self._add_two_factor()
        self.assertIn(self._get(basic()).status_code, (401, 403))

    def test_the_refusal_looks_like_a_wrong_password(self):
        self._add_two_factor()
        refused = self._get(basic())
        wrong = self._get(basic(password="not-the-password"))

        self.assertEqual(refused.status_code, wrong.status_code)
        self.assertEqual(refused.content, wrong.content)

    def test_an_unconfirmed_device_does_not_lock_the_user_out(self):
        TOTPDevice.objects.create(user=User.objects.get(username=USERNAME), name="half set up", confirmed=False)
        self.assertEqual(self._get(basic()).status_code, 200)

    def test_two_factor_on_one_user_does_not_affect_another(self):
        self._add_two_factor("admin")
        self.assertEqual(self._get(basic()).status_code, 200)

    def test_the_login_page_still_works_with_two_factor(self):
        device = self._add_two_factor()
        response = APIClient().post(
            LOGIN_URL,
            {"username": USERNAME, "password": PASSWORD, "otp_token": totp_token(device)},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")


class ThrottleAddressTests(LoginHardeningTestBase):
    """The login rate limit is only worth anything if a visitor can not pick their own address"""

    def _attempts(self, count, **extra_for):
        statuses = []
        for index in range(count):
            extra = extra_for["extra"](index) if "extra" in extra_for else {}
            statuses.append(APIClient().post(
                LOGIN_URL, {"username": USERNAME, "password": "wrong", "otp_token": ""}, format="json", **extra,
            ).status_code)
        return statuses

    def test_the_default_ignores_x_forwarded_for(self):
        self._rates(minute="3/min")

        statuses = self._attempts(6, extra=lambda i: {"HTTP_X_FORWARDED_FOR": f"10.0.0.{i}"})

        self.assertEqual(statuses[:3], [401, 401, 401])
        self.assertEqual(statuses[3:], [429, 429, 429])

    def test_the_setting_defaults_to_no_trusted_proxies(self):
        self.assertEqual(settings.REST_FRAMEWORK["NUM_PROXIES"], 0)

    def test_behind_one_proxy_the_address_it_added_is_used(self):
        self._rates(minute="3/min")
        rest = {**settings.REST_FRAMEWORK, "NUM_PROXIES": 1}

        with override_settings(REST_FRAMEWORK=rest):
            # A visitor can make up the first address, but the proxy always adds the real one last
            fakes = self._attempts(6, extra=lambda i: {
                "HTTP_X_FORWARDED_FOR": f"10.9.9.{i}, 203.0.113.7", "REMOTE_ADDR": "10.0.0.1"})
            other = self._attempts(1, extra=lambda i: {
                "HTTP_X_FORWARDED_FOR": "1.1.1.1, 203.0.113.99", "REMOTE_ADDR": "10.0.0.1"})

        self.assertEqual(fakes, [401, 401, 401, 429, 429, 429])
        self.assertEqual(other, [401])


class AdminLoginTests(LoginHardeningTestBase):
    """The Django admin login is a second way in with a password - it needs the same protection"""

    def _post(self, username="admin", password=PASSWORD, otp_token="", client=None):
        return (client or Client()).post(
            ADMIN_LOGIN_URL + "?next=/admin/",
            {"username": username, "password": password, "otp_token": otp_token, "next": "/admin/"},
        )

    def test_a_user_without_two_factor_can_sign_in(self):
        response = self._post()
        self.assertEqual(response.status_code, 302)

    def test_the_page_asks_for_a_two_factor_code(self):
        response = Client().get(ADMIN_LOGIN_URL)
        self.assertContains(response, 'name="otp_token"')

    def test_a_user_with_two_factor_is_not_let_in_by_password_alone(self):
        self._add_two_factor("admin")
        client = Client()

        response = self._post(client=client)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter your two-factor code.")
        self.assertNotIn("_auth_user_id", client.session)

    def test_a_wrong_two_factor_code_is_refused(self):
        self._add_two_factor("admin")
        client = Client()

        response = self._post(otp_token="000000", client=client)

        self.assertContains(response, "That two-factor code is not valid.")
        self.assertNotIn("_auth_user_id", client.session)

    def test_the_right_two_factor_code_signs_in(self):
        device = self._add_two_factor("admin")
        client = Client()

        response = self._post(otp_token=totp_token(device), client=client)

        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", client.session)

    def test_a_wrong_password_never_reaches_the_two_factor_check(self):
        self._add_two_factor("admin")
        response = self._post(password="wrong")
        self.assertNotContains(response, "two-factor code")

    def test_signing_in_is_rate_limited(self):
        self._rates(minute="3/min")

        statuses = [self._post(password="wrong").status_code for _ in range(5)]

        self.assertEqual(statuses[:3], [200, 200, 200])
        self.assertEqual(statuses[3:], [429, 429])

    def test_looking_at_the_page_is_not_rate_limited(self):
        self._rates(minute="1/min")
        self.assertEqual([Client().get(ADMIN_LOGIN_URL).status_code for _ in range(4)], [200] * 4)

    def test_the_admin_limit_is_separate_from_the_main_login_limit(self):
        self._rates(minute="3/min")
        for _ in range(3):
            APIClient().post(LOGIN_URL, {"username": USERNAME, "password": "x", "otp_token": ""}, format="json")

        self.assertEqual(self._post(password="wrong").status_code, 200)
