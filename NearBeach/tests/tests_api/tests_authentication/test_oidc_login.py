import time
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from django.contrib.auth.models import User
from django.core.cache import cache
from django_otp.plugins.otp_totp.models import TOTPDevice
from joserfc import jwt
from joserfc.jwk import RSAKey

from NearBeach.models.authentication.oidc_provider import OidcIdentity, OidcProvider
from NearBeach.models.permission.group import Group
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.user import UserGroup
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

ISSUER = "https://idp.example.com/realms/nearbeach"
CLIENT_ID = "nearbeach"
USERNAME = "team_member"
METADATA = {
    "issuer": ISSUER,
    "authorization_endpoint": f"{ISSUER}/auth",
    "token_endpoint": f"{ISSUER}/token",
    "jwks_uri": f"{ISSUER}/certs",
}


class OidcLoginTests(BaseApiClass):
    """Tests for single sign-on through an OpenID Connect provider

    Notes
    ~~~~~
    - No network: discovery/JWKS are patched and the token endpoint returns an ID token we sign ourselves
    - Every callback goes through `_complete_login`, so each test only states how it differs from a good sign in
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.key = RSAKey.generate_key(2048, parameters={"kid": "test-key", "use": "sig"})

    def setUp(self):
        super().setUp()
        cache.clear()

        self.provider = OidcProvider.objects.create(
            name="Keycloak",
            slug="keycloak",
            issuer_url=ISSUER,
            client_id=CLIENT_ID,
            client_secret="secret",
        )

        # The views' own throttles are not what is under test
        for view in ("OidcLoginView", "OidcCallbackView"):
            patcher = patch(
                f"NearBeach.views.api_v1.authentication.oidc_api_view.{view}.throttle_classes", []
            )
            patcher.start()
            self.addCleanup(patcher.stop)

        patcher = patch(
            "NearBeach.services.OidcService.OidcService._get_json",
            side_effect=lambda url: {"keys": [self.key.as_dict(private=False)]} if url.endswith("/certs") else METADATA,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    # ---------- helpers ----------
    def _id_token(self, nonce, **overrides):
        claims = {
            "iss": ISSUER,
            "aud": CLIENT_ID,
            "sub": "subject-1",
            "exp": int(time.time()) + 300,
            "iat": int(time.time()),
            "nonce": nonce,
            "email": "sso.user@example.com",
            "email_verified": True,
            "preferred_username": "sso.user",
            "given_name": "Sso",
            "family_name": "User",
        }
        claims.update(overrides)
        return jwt.encode({"alg": "RS256", "kid": "test-key"}, claims, self.key)

    def _start(self, query=""):
        response = self.client.get(f"/api/v1/authentication/oidc/keycloak/login/{query}")
        self.assertEqual(response.status_code, 302)
        return response

    def _complete_login(self, claims=None, nonce=None, state=None, id_token=None):
        """Run the whole flow, returning the callback response"""
        self._start()
        flow = self.client.session["oidc_flow"]

        token = id_token or self._id_token(nonce or flow["nonce"], **(claims or {}))
        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"id_token": token},
        ):
            return self.client.get(
                "/api/v1/authentication/oidc/keycloak/callback/",
                {"code": "abc", "state": state or flow["state"]},
            )

    def _link_identity(self, username=USERNAME, subject="subject-1"):
        user = User.objects.get(username=username)
        OidcIdentity.objects.create(user=user, provider=self.provider, subject=subject, change_user=user)
        return user

    def _assert_failed(self, response, code):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/login/?sso_error={code}")
        self.assertNotIn("_auth_user_id", self.client.session)

    def _assert_logged_in_as(self, response, user, url="/"):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    def _enable_auto_create(self):
        self.provider.auto_create_users = True
        self.provider.default_group = Group.objects.first()
        self.provider.default_permission_set = PermissionSet.objects.first()
        self.provider.save()

    # ---------- providers list ----------
    def test_providers_lists_only_enabled(self):
        OidcProvider.objects.create(name="Off", slug="off", issuer_url=ISSUER, client_id="x", is_enabled=False)

        response = self.client.get("/api/v1/authentication/oidc/providers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"name": "Keycloak", "slug": "keycloak", "login_url": "/api/v1/authentication/oidc/keycloak/login/"}],
        )

    def test_providers_never_exposes_the_secret(self):
        response = self.client.get("/api/v1/authentication/oidc/providers/")
        self.assertNotIn("secret", response.content.decode())

    # ---------- start ----------
    def test_login_redirects_to_provider_with_pkce(self):
        response = self._start()
        url = urlparse(response.url)
        query = parse_qs(url.query)

        self.assertEqual(f"{url.scheme}://{url.netloc}{url.path}", METADATA["authorization_endpoint"])
        self.assertEqual(query["client_id"], [CLIENT_ID])
        self.assertEqual(query["response_type"], ["code"])
        self.assertEqual(query["code_challenge_method"], ["S256"])
        self.assertEqual(query["state"], [self.client.session["oidc_flow"]["state"]])
        self.assertEqual(query["nonce"], [self.client.session["oidc_flow"]["nonce"]])

    def test_login_unknown_or_disabled_provider_is_404(self):
        self.provider.is_enabled = False
        self.provider.save()
        response = self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        self.assertEqual(response.status_code, 404)

    def test_login_provider_unreachable_goes_back_to_login(self):
        with patch(
            "NearBeach.services.OidcService.OidcService._get_json",
            side_effect=__import__("NearBeach.services.OidcService", fromlist=["OidcError"]).OidcError(
                "provider_unavailable"
            ),
        ):
            response = self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        self.assertEqual(response.url, "/login/?sso_error=provider_unavailable")

    # ---------- callback: success ----------
    def test_known_identity_logs_in(self):
        user = self._link_identity()
        self._assert_logged_in_as(self._complete_login(), user)

    def test_next_url_is_followed_when_local(self):
        user = self._link_identity()
        self._start("?next=/some/page/")
        flow = self.client.session["oidc_flow"]
        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"id_token": self._id_token(flow["nonce"])},
        ):
            response = self.client.get(
                "/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": flow["state"]}
            )
        self._assert_logged_in_as(response, user, "/some/page/")

    def test_next_url_to_another_site_is_ignored(self):
        self._start("?next=https://evil.example.com/")
        self.assertEqual(self.client.session["oidc_flow"]["next"], "/")

    # ---------- callback: rejected ----------
    def test_wrong_state_is_rejected(self):
        self._link_identity()
        self._assert_failed(self._complete_login(state="not-the-state"), "invalid_state")

    def test_callback_without_starting_is_rejected(self):
        response = self.client.get("/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": "x"})
        self._assert_failed(response, "invalid_state")

    def test_state_cannot_be_replayed(self):
        self._link_identity()
        self._start()
        flow = self.client.session["oidc_flow"]
        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"id_token": self._id_token(flow["nonce"])},
        ):
            params = {"code": "abc", "state": flow["state"]}
            self.client.get("/api/v1/authentication/oidc/keycloak/callback/", params)
            self.client.logout()
            replay = self.client.get("/api/v1/authentication/oidc/keycloak/callback/", params)
        self._assert_failed(replay, "invalid_state")

    def test_provider_error_is_rejected(self):
        self._start()
        response = self.client.get("/api/v1/authentication/oidc/keycloak/callback/", {"error": "access_denied"})
        self._assert_failed(response, "provider_denied")

    def test_id_token_rejections(self):
        self._link_identity()
        cases = {
            "wrong nonce": {"nonce": "attacker-nonce"},
            "wrong audience": {"claims": {"aud": "someone-else"}},
            "wrong issuer": {"claims": {"iss": "https://evil.example.com"}},
            "expired": {"claims": {"exp": int(time.time()) - 3600}},
        }
        for name, kwargs in cases.items():
            with self.subTest(name):
                self.client.logout()
                self._assert_failed(self._complete_login(**kwargs), "invalid_id_token")

    def test_id_token_signed_by_another_key_is_rejected(self):
        self._link_identity()
        other = RSAKey.generate_key(2048, parameters={"kid": "test-key"})
        self._start()
        forged = jwt.encode(
            {"alg": "RS256", "kid": "test-key"},
            {"iss": ISSUER, "aud": CLIENT_ID, "sub": "subject-1", "exp": int(time.time()) + 300,
             "nonce": self.client.session["oidc_flow"]["nonce"]},
            other,
        )
        self.client.logout()
        self._assert_failed(self._complete_login(id_token=forged), "invalid_id_token")

    def test_failed_token_exchange_is_rejected(self):
        self._start()
        flow = self.client.session["oidc_flow"]
        with patch("authlib.integrations.requests_client.OAuth2Session.fetch_token", side_effect=Exception("nope")):
            response = self.client.get(
                "/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": flow["state"]}
            )
        self._assert_failed(response, "token_exchange_failed")

    # ---------- user resolution ----------
    def test_unknown_user_without_auto_create_is_rejected(self):
        self._assert_failed(self._complete_login(), "no_account")
        self.assertFalse(User.objects.filter(username="sso.user").exists())

    def test_auto_create_makes_user_group_and_identity(self):
        self._enable_auto_create()

        response = self._complete_login()

        user = User.objects.get(username="sso.user")
        self._assert_logged_in_as(response, user)
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.email, "sso.user@example.com")
        self.assertTrue(UserGroup.objects.filter(username=user, group=self.provider.default_group).exists())
        self.assertTrue(OidcIdentity.objects.filter(user=user, provider=self.provider, subject="subject-1").exists())

    def test_auto_create_needs_a_default_group(self):
        self.provider.auto_create_users = True
        self.provider.save()
        self._assert_failed(self._complete_login(), "no_account")

    def test_auto_create_does_not_take_an_existing_username(self):
        self._enable_auto_create()
        self._complete_login(claims={"preferred_username": USERNAME})
        self.assertTrue(User.objects.filter(username=f"{USERNAME}-2").exists())

    def test_auto_create_drops_an_unverified_email(self):
        self._enable_auto_create()
        self._complete_login(claims={"email_verified": False})
        self.assertEqual(User.objects.get(username="sso.user").email, "")

    def test_link_existing_user_by_verified_email(self):
        self.provider.link_existing_by_email = True
        self.provider.save()
        user = User.objects.get(username=USERNAME)
        user.email = "sso.user@example.com"
        user.save()

        self._assert_logged_in_as(self._complete_login(), user)
        self.assertTrue(OidcIdentity.objects.filter(user=user, subject="subject-1").exists())

    def test_unverified_email_never_links(self):
        self.provider.link_existing_by_email = True
        self.provider.save()
        user = User.objects.get(username=USERNAME)
        user.email = "sso.user@example.com"
        user.save()

        self._assert_failed(self._complete_login(claims={"email_verified": False}), "no_account")
        self.assertFalse(OidcIdentity.objects.exists())

    def test_email_is_not_linked_unless_enabled(self):
        user = User.objects.get(username=USERNAME)
        user.email = "sso.user@example.com"
        user.save()
        self._assert_failed(self._complete_login(), "no_account")

    def test_email_shared_by_two_users_never_links(self):
        self.provider.link_existing_by_email = True
        self.provider.save()
        User.objects.filter(username__in=[USERNAME, "admin"]).update(email="sso.user@example.com")
        self._assert_failed(self._complete_login(), "no_account")

    def test_user_without_a_group_is_rejected(self):
        user = self._link_identity()
        UserGroup.objects.filter(username=user).delete()
        self._assert_failed(self._complete_login(), "no_group")

    def test_inactive_user_is_rejected(self):
        user = self._link_identity()
        user.is_active = False
        user.save()
        self._assert_failed(self._complete_login(), "account_disabled")

    # ---------- two factor ----------
    def test_user_with_two_factor_is_refused_unless_provider_is_trusted(self):
        user = self._link_identity()
        TOTPDevice.objects.create(user=user, name="phone", confirmed=True)

        self._assert_failed(self._complete_login(), "two_factor_required")

    def test_user_with_two_factor_signs_in_when_provider_mfa_is_trusted(self):
        user = self._link_identity()
        TOTPDevice.objects.create(user=user, name="phone", confirmed=True)
        self.provider.trust_idp_mfa = True
        self.provider.save()

        self._assert_logged_in_as(self._complete_login(), user)
