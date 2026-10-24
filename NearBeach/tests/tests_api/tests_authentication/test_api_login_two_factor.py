import time

from django.contrib.auth.models import User
from django.core import mail
from django.utils import timezone
from django_otp.oath import TOTP
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice

from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.enums.login_status_enum import LoginStatusEnum

LOGIN_URL = "/api/v1/authentication/"
USERNAME = "team_member"
PASSWORD = "Test1234$"


class ApiAuthenticationTwoFactorTests(BaseApiClass):
    """Two-factor tests - TOTP (authenticator app) and Email devices

    Notes
    ~~~~~
    - No username on the class, so BaseApiClass does not log in for us
    - Django swaps the email backend for locmem during tests, so sent emails are in `mail.outbox`
    - TOTP tokens are calculated from the device key with the same algorithm the authenticator app uses
    """

    # ---------- helpers ----------
    @staticmethod
    def _user(username=USERNAME):
        return User.objects.get(username=username)

    def _create_totp_device(self, username=USERNAME, confirmed=True):
        return TOTPDevice.objects.create(
            user=self._user(username),
            name="test totp",
            confirmed=confirmed,
        )

    def _create_email_device(self, username=USERNAME, confirmed=True):
        user = self._user(username)
        return EmailDevice.objects.create(
            user=user,
            name="test email",
            email=user.email or "team_member@example.com",
            confirmed=confirmed,
        )

    @staticmethod
    def _totp_token(device, step_offset=0) -> str:
        """The token an authenticator app would currently show for this device"""
        totp = TOTP(
            key=device.bin_key,
            step=device.step,
            t0=device.t0,
            digits=device.digits,
        )
        totp.time = time.time() + (step_offset * device.step)
        return str(totp.token()).zfill(device.digits)

    def _login(self, otp_token="", username=USERNAME, password=PASSWORD):
        return self.client.post(
            LOGIN_URL,
            {"username": username, "password": password, "otp_token": otp_token},
            format="json",
        )

    def _assert_logged_in(self):
        self.assertEqual(self.client.get("/api/v1/project/").status_code, 200)

    def _assert_not_logged_in(self):
        self.assertEqual(self.client.get("/api/v1/project/").status_code, 403)

    # ---------- no 2FA ----------
    def test_no_device_logs_in_without_token(self):
        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.SUCCESS)
        self._assert_logged_in()

    def test_unconfirmed_devices_do_not_require_two_factor(self):
        """A device that was never confirmed (setup abandoned) must not lock the user out"""
        self._create_totp_device(confirmed=False)
        self._create_email_device(confirmed=False)

        response = self._login()
        self.assertEqual(response.data["status"], LoginStatusEnum.SUCCESS)
        self._assert_logged_in()

    def test_missing_otp_token_field_is_bad_request(self):
        response = self.client.post(
            LOGIN_URL, {"username": USERNAME, "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    # ---------- TOTP ----------
    def test_totp_without_token_asks_for_two_factor(self):
        self._create_totp_device()

        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.TWO_FACTOR_REQUIRED)
        # Password alone must NOT create a session
        self._assert_not_logged_in()

    def test_totp_correct_token_logs_in(self):
        device = self._create_totp_device()

        response = self._login(self._totp_token(device))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.SUCCESS)
        self._assert_logged_in()

    def test_totp_wrong_token_is_rejected(self):
        device = self._create_totp_device()
        good = self._totp_token(device)
        bad = str((int(good) + 1) % 10 ** device.digits).zfill(device.digits)

        response = self._login(bad)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["status"], LoginStatusEnum.FAILURE)
        self._assert_not_logged_in()

    def test_totp_garbage_tokens_are_rejected(self):
        self._create_totp_device()
        for token in ["abc", "000000000000", "!@#$%^", "0" * 6]:
            with self.subTest(token=token):
                response = self._login(token)
                self.assertEqual(response.status_code, 403)
                self._assert_not_logged_in()

    def test_totp_whitespace_token_is_treated_as_no_token(self):
        """DRF trims the CharField, so ' ' becomes '' and the user is simply asked for a code"""
        self._create_totp_device()

        response = self._login(" ")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.TWO_FACTOR_REQUIRED)
        self._assert_not_logged_in()

    def test_totp_token_cannot_be_replayed(self):
        """django-otp stores last_t - the same code must not work twice"""
        device = self._create_totp_device()
        token = self._totp_token(device)

        self.assertEqual(self._login(token).status_code, 200)

        self.client.logout()
        self.assertEqual(self._login(token).status_code, 403)
        self._assert_not_logged_in()

    def test_totp_token_far_outside_window_is_rejected(self):
        device = self._create_totp_device()
        old_token = self._totp_token(device, step_offset=-10)  # 5 minutes ago

        response = self._login(old_token)
        self.assertEqual(response.status_code, 403)

    def test_totp_token_belonging_to_another_user_is_rejected(self):
        other_device = self._create_totp_device(username="team_leader")
        self._create_totp_device(username=USERNAME)

        response = self._login(self._totp_token(other_device))
        self.assertEqual(response.status_code, 403)
        self._assert_not_logged_in()

    def test_two_factor_only_applies_to_the_user_with_a_device(self):
        self._create_totp_device(username="team_leader")

        # team_member has no device - unaffected
        self.assertEqual(self._login().data["status"], LoginStatusEnum.SUCCESS)

    # ---------- password still checked first ----------
    def test_wrong_password_with_two_factor_never_reaches_token_stage(self):
        device = self._create_totp_device()
        self._create_email_device()

        response = self._login(self._totp_token(device), password="wrong")
        # NOTE: the 401 body carries no `status` key (serializer.data has no such field)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(mail.outbox), 0, "No email token should go out for a bad password")
        self._assert_not_logged_in()

    def test_user_without_groups_cannot_log_in_even_with_valid_token(self):
        device = self._create_totp_device(username="no_group")

        response = self._login(
            self._totp_token(device), username="no_group", password=PASSWORD
        )
        self.assertEqual(response.status_code, 401)

    # ---------- Email ----------
    def test_email_device_sends_token_when_none_supplied(self):
        self._create_email_device()

        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.TWO_FACTOR_REQUIRED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "NearBeach 2FA")
        self._assert_not_logged_in()

    def test_email_device_correct_token_logs_in(self):
        device = self._create_email_device()
        self._login()  # triggers the email + stores the token
        device.refresh_from_db()
        self.assertTrue(device.token)

        response = self._login(device.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], LoginStatusEnum.SUCCESS)
        self._assert_logged_in()

    def test_email_device_wrong_token_is_rejected(self):
        device = self._create_email_device()
        self._login()
        device.refresh_from_db()
        wrong = "0" * len(device.token) if device.token != "0" * len(device.token) else "1" * len(device.token)

        response = self._login(wrong)
        self.assertEqual(response.status_code, 403)
        self._assert_not_logged_in()

    def test_email_device_expired_token_is_rejected(self):
        device = self._create_email_device()
        self._login()
        device.refresh_from_db()
        device.valid_until = timezone.now() - timezone.timedelta(minutes=1)
        device.save()

        response = self._login(device.token)
        self.assertEqual(response.status_code, 403)
        self._assert_not_logged_in()

    def test_email_device_token_cannot_be_reused(self):
        device = self._create_email_device()
        self._login()
        device.refresh_from_db()
        token = device.token

        self.assertEqual(self._login(token).status_code, 200)
        self.client.logout()
        self.assertEqual(self._login(token).status_code, 403)

    def test_supplying_a_token_does_not_send_another_email(self):
        device = self._create_email_device()
        self._login()
        device.refresh_from_db()
        mail.outbox.clear()

        self._login(device.token)
        self.assertEqual(len(mail.outbox), 0)

    # ---------- both devices ----------
    def test_user_with_both_devices_can_use_either(self):
        totp_device = self._create_totp_device()
        email_device = self._create_email_device()

        # Authenticator app code
        self.assertEqual(self._login(self._totp_token(totp_device)).status_code, 200)
        self.client.logout()

        # Email code
        self._login()
        email_device.refresh_from_db()
        self.assertEqual(self._login(email_device.token).status_code, 200)

    # ---------- known behaviour to decide on ----------
    def test_static_backup_device_alone_does_not_enforce_two_factor(self):
        """_check_user_two_factor_devices only looks at TOTP + Email devices.

        A user with ONLY a StaticDevice (backup codes) is therefore logged in with just a password.
        Documenting current behaviour - change the assertion if that is not intended.
        """
        StaticDevice.objects.create(user=self._user(), name="backup", confirmed=True)

        response = self._login()
        self.assertEqual(response.data["status"], LoginStatusEnum.SUCCESS)
