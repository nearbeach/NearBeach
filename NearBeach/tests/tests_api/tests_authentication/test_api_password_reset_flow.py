"""Forgotten password -> email -> reset page -> new password.

This answers the TODOs in test_api_reset_password.py ("how can we get the token?"): either read the link out of the
email in `mail.outbox`, or make one the same way the view does - the user's id, base64 encoded, and a
PasswordResetTokenGenerator token.
"""
import re
from datetime import datetime, timedelta
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.core.cache import cache
from django.test import Client
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.throttling import SimpleRateThrottle

from NearBeach.services.AsyncEmailService import AsyncEmailService
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

FORGOTTEN_URL = "/api/v1/authentication/forgotten-password/"
RESET_API_URL = "/api/v1/authentication/reset-password/"
RESET_PAGE_URL = "/login/reset-password/"
LOGIN_URL = "/api/v1/authentication/"
USERNAME = "team_member"
OLD_PASSWORD = "Test1234$"
NEW_PASSWORD = "A-brand-new-Passphrase-42"
SHARED_EMAIL = "support@nearbeach.org"  # every fixture user has this address


class PasswordResetTestBase(BaseApiClass):
    def setUp(self):
        super().setUp()
        # These views are throttled - clear the history and lift the rate so many requests do not matter here
        cache.clear()
        self.addCleanup(cache.clear)
        rates = mock.patch.dict(
            SimpleRateThrottle.THROTTLE_RATES, {"auth_minute": "100000/min", "auth_hour": "100000/hour"}
        )
        rates.start()
        self.addCleanup(rates.stop)

        # The email is sent from a thread - send it straight away so the test can read it
        sync = mock.patch.object(AsyncEmailService, "start", AsyncEmailService.run)
        sync.start()
        self.addCleanup(sync.stop)

    @staticmethod
    def _user(username=USERNAME):
        return User.objects.get(username=username)

    @staticmethod
    def _uid(user):
        return urlsafe_base64_encode(force_bytes(user.pk))

    def _link(self, user):
        """A valid (uid, token) pair for a user"""
        return self._uid(user), PasswordResetTokenGenerator().make_token(user)

    def _reset(self, uid, token, password=NEW_PASSWORD, client=None):
        return (client or self.client).post(
            RESET_API_URL, {"uid": uid, "token": token, "password": password}, format="json"
        )

    def _can_log_in(self, password, username=USERNAME):
        return Client().post(
            LOGIN_URL,
            {"username": username, "password": password, "otp_token": ""},
            content_type="application/json",
        ).status_code == 200


class ForgottenPasswordEmailTests(PasswordResetTestBase):
    def _forgot(self, email):
        return self.client.post(FORGOTTEN_URL, {"email": email}, format="json")

    def test_every_active_user_with_the_email_gets_a_reset_email(self):
        active = User.objects.filter(email=SHARED_EMAIL, is_active=True).count()

        response = self._forgot(SHARED_EMAIL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), active)
        for message in mail.outbox:
            self.assertEqual(message.to, [SHARED_EMAIL])
            self.assertEqual(message.subject, "NearBeach Password Reset")

    def test_inactive_users_get_nothing(self):
        active = User.objects.filter(email=SHARED_EMAIL, is_active=True).count()
        User.objects.filter(username=USERNAME).update(is_active=False)

        self._forgot(SHARED_EMAIL)

        self.assertEqual(len(mail.outbox), active - 1)

    def test_an_unknown_email_looks_exactly_like_a_known_one(self):
        """Otherwise the form tells an attacker which addresses have accounts"""
        known = self._forgot(SHARED_EMAIL)
        unknown = self._forgot("nobody-has-this@example.org")

        self.assertEqual(known.status_code, unknown.status_code)
        self.assertEqual(known.content, unknown.content)

    def test_an_unknown_email_sends_nothing(self):
        self._forgot("nobody-has-this@example.org")

        self.assertEqual(len(mail.outbox), 0)

    def test_bad_requests_are_rejected_and_send_nothing(self):
        for name, body in {"not an email": {"email": "nope"}, "empty": {"email": ""}, "missing": {}}.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(FORGOTTEN_URL, body, format="json").status_code, 400)

        self.assertEqual(len(mail.outbox), 0)

    def test_the_link_in_the_email_resets_the_password(self):
        """The whole journey: email -> reset page -> new password -> log in"""
        self._forgot(SHARED_EMAIL)
        html = next(
            message.alternatives[0][0]
            for message in mail.outbox
            if User.objects.filter(email=message.to[0]).count() > 0
        )
        link = re.search(r'(http://testserver/login/reset-password/\?uid=[^&"\']+&(?:amp;)?token=[^"\'<\s]+)', html)
        self.assertIsNotNone(link, "The email has no reset link")
        uid, token = re.search(r"uid=([^&]+)&(?:amp;)?token=(.+)", link.group(1)).groups()
        target = User.objects.get(pk=int(urlsafe_b64(uid)))

        self.assertEqual(self.client.get(RESET_PAGE_URL, {"uid": uid, "token": token}).status_code, 200)
        self.assertEqual(self._reset(uid, token).status_code, 200)

        target.refresh_from_db()
        self.assertTrue(target.check_password(NEW_PASSWORD))


def urlsafe_b64(uid):
    from django.utils.encoding import force_str
    from django.utils.http import urlsafe_base64_decode

    return force_str(urlsafe_base64_decode(uid))


class PasswordResetApiTests(PasswordResetTestBase):
    def test_a_valid_link_sets_the_new_password(self):
        uid, token = self._link(self._user())

        response = self._reset(uid, token)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._can_log_in(NEW_PASSWORD))
        self.assertFalse(self._can_log_in(OLD_PASSWORD))

    def test_a_link_only_works_once(self):
        uid, token = self._link(self._user())
        self.assertEqual(self._reset(uid, token).status_code, 200)

        again = self._reset(uid, token, password="Another-Passphrase-77")

        self.assertEqual(again.status_code, 403)
        self.assertTrue(self._can_log_in(NEW_PASSWORD))

    def test_an_expired_link_is_rejected(self):
        uid, token = self._link(self._user())
        later = datetime.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT + 60)

        with mock.patch.object(PasswordResetTokenGenerator, "_now", return_value=later):
            response = self._reset(uid, token)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(self._can_log_in(OLD_PASSWORD))

    def test_a_link_still_works_just_before_it_expires(self):
        uid, token = self._link(self._user())
        later = datetime.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT - 60)

        with mock.patch.object(PasswordResetTokenGenerator, "_now", return_value=later):
            response = self._reset(uid, token)

        self.assertEqual(response.status_code, 200)

    def test_a_wrong_token_is_rejected(self):
        uid, _ = self._link(self._user())

        for token in ["not-a-token", "000-0000", ""]:
            with self.subTest(token=token):
                self.assertIn(self._reset(uid, token).status_code, (400, 403))

        self.assertTrue(self._can_log_in(OLD_PASSWORD))

    def test_one_users_token_can_not_reset_another_user(self):
        _, leader_token = self._link(self._user("team_leader"))
        member_uid = self._uid(self._user())

        self.assertEqual(self._reset(member_uid, leader_token).status_code, 403)
        self.assertTrue(self._can_log_in(OLD_PASSWORD))

    def test_a_reset_only_changes_the_one_user(self):
        others = {u.username: u.password for u in User.objects.exclude(username=USERNAME)}
        uid, token = self._link(self._user())

        self._reset(uid, token)

        for user in User.objects.exclude(username=USERNAME):
            with self.subTest(username=user.username):
                self.assertEqual(user.password, others[user.username])

    def test_unknown_and_inactive_users_look_like_a_success_but_change_nothing(self):
        """The reply must not tell an attacker whether the user exists"""
        inactive = self._user("read_only")
        uid, token = self._link(inactive)
        User.objects.filter(pk=inactive.pk).update(is_active=False)

        replies = {
            "unknown user": self._reset(urlsafe_base64_encode(force_bytes(999999)), "abc-123"),
            "inactive user": self._reset(uid, token),
        }

        for name, response in replies.items():
            with self.subTest(name):
                self.assertEqual(response.status_code, 200)

        inactive.refresh_from_db()
        self.assertTrue(inactive.check_password(OLD_PASSWORD))

    def test_a_garbage_uid_is_never_a_server_error(self):
        for uid in ["!!!", "abc", "ZZZ", "%%", "a" * 500, "_-_-", urlsafe_base64_encode(b"not-a-number"),
                    urlsafe_base64_encode(b"\xff\xfe")]:
            with self.subTest(uid=uid):
                response = self._reset(uid, "abc-123")

                self.assertEqual(response.status_code, 200)

    def test_weak_new_passwords_are_rejected(self):
        uid, token = self._link(self._user())
        hash_before = self._user().password

        weak = {
            "too short": "Ab1!",
            "all numbers": "1234567890123",
            "too common": "password123",
            "the username": USERNAME,
        }
        for name, password in weak.items():
            with self.subTest(name):
                response = self._reset(uid, token, password=password)

                self.assertEqual(response.status_code, 400)
                self.assertIn("password", response.data)

        # Nothing was used up or changed - the link still works with a good password.
        # (Compare the stored hash: logging in, or even check_password, can change it or last_login -
        # both are part of the token)
        self.assertEqual(self._user().password, hash_before)
        self.assertEqual(self._reset(uid, token).status_code, 200)

    def test_missing_fields_are_rejected(self):
        uid, token = self._link(self._user())
        bodies = {
            "no uid": {"token": token, "password": NEW_PASSWORD},
            "no token": {"uid": uid, "password": NEW_PASSWORD},
            "no password": {"uid": uid, "token": token},
            "empty password": {"uid": uid, "token": token, "password": ""},
            "nothing": {},
        }
        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(RESET_API_URL, body, format="json").status_code, 400)

        self.assertTrue(self._can_log_in(OLD_PASSWORD))

    def test_resetting_signs_the_user_out_everywhere(self):
        """If someone else has the old password, the reset should end their session"""
        other_session = Client()
        self.assertTrue(other_session.login(username=USERNAME, password=OLD_PASSWORD))
        self.assertEqual(other_session.get("/api/v1/project/").status_code, 200)
        uid, token = self._link(self._user())

        self._reset(uid, token)

        self.assertEqual(other_session.get("/api/v1/project/").status_code, 403)


class ResetPasswordPageTests(PasswordResetTestBase):
    def _page(self, **params):
        return self.client.get(RESET_PAGE_URL, params)

    def _assert_sent_to_login(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_a_valid_link_shows_the_page(self):
        uid, token = self._link(self._user())

        response = self._page(uid=uid, token=token)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "NearBeach/authentication/authentication.html")

    def test_missing_parameters_go_to_the_login_page(self):
        uid, token = self._link(self._user())

        for name, params in {"nothing": {}, "no token": {"uid": uid}, "no uid": {"token": token}}.items():
            with self.subTest(name):
                self._assert_sent_to_login(self._page(**params))

    def test_bad_links_go_to_the_login_page(self):
        uid, token = self._link(self._user())
        later = datetime.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT + 60)

        self._assert_sent_to_login(self._page(uid=uid, token="not-a-token"))
        self._assert_sent_to_login(self._page(uid=urlsafe_base64_encode(force_bytes(999999)), token=token))
        with mock.patch.object(PasswordResetTokenGenerator, "_now", return_value=later):
            self._assert_sent_to_login(self._page(uid=uid, token=token))

    def test_a_garbage_uid_goes_to_the_login_page(self):
        for uid in ["!!!", "abc", "a" * 500, urlsafe_base64_encode(b"not-a-number")]:
            with self.subTest(uid=uid):
                self._assert_sent_to_login(self._page(uid=uid, token="abc-123"))

    def test_a_used_link_goes_to_the_login_page(self):
        uid, token = self._link(self._user())
        self._reset(uid, token)

        self._assert_sent_to_login(self._page(uid=uid, token=token))

    def test_an_inactive_user_goes_to_the_login_page(self):
        user = self._user()
        uid, token = self._link(user)
        User.objects.filter(pk=user.pk).update(is_active=False)

        self._assert_sent_to_login(self._page(uid=uid, token=token))
