import base64
import hashlib
from datetime import timedelta
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.throttling import SimpleRateThrottle

from NearBeach.api_docs.extensions import NearBeachOAuth2Scheme  # noqa: F401
from NearBeach.models.misc.misc import ExtendsAuthToken
from NearBeach.models.user import UserGroup
from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.oauth2.authentication import NearBeachOAuth2Authentication
from NearBeach.utils.oauth2.permissions import OAuth2ScopePermission

TOKEN_URL = "/o/token/"
READ_URL = "/api/v1/user/initial_data/"
WRITE_URL = "/api/v1/project/"
SERVICE_USER = "team_member"
SCOPE_MESSAGE = "does not have the scope"


class OAuth2ProviderTests(BaseApiClass):
    """Tests for NearBeach acting as an OAuth2 provider for its API

    Notes
    ~~~~~
    - No username on the class, so the test client starts anonymous - these requests must stand on their token alone
    - The service user is `team_member`, who is already in a group in the fixture
    """

    def setUp(self):
        super().setUp()
        cache.clear()
        self.service_user = User.objects.get(username=SERVICE_USER)
        self.secret = "a-very-long-client-secret"
        self.application = Application.objects.create(
            name="Reporting integration",
            user=self.service_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_secret=self.secret,
        )

    # ---------- helpers ----------
    def _token(self, scope="read", application=None, secret=None):
        application = application or self.application
        return self.client.post(
            TOKEN_URL,
            {
                "grant_type": "client_credentials",
                "client_id": application.client_id,
                "client_secret": secret or self.secret,
                "scope": scope,
            },
        )

    def _bearer(self, scope="read"):
        response = self._token(scope)
        self.assertEqual(response.status_code, 200, response.content)
        return {"HTTP_AUTHORIZATION": f"Bearer {response.json()['access_token']}"}

    def _get(self, headers, url=READ_URL):
        return APIClient().get(url, **headers)

    # ---------- getting a token ----------
    def test_client_credentials_returns_a_bearer_token(self):
        response = self._token("read")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["token_type"], "Bearer")
        self.assertEqual(body["scope"], "read")
        self.assertEqual(body["expires_in"], 3600)

    def test_wrong_secret_gets_no_token(self):
        response = self._token(secret="not-the-secret")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access_token", response.json())

    def test_unknown_scope_gets_no_token(self):
        response = self._token("read admin")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "invalid_scope")

    def test_client_secret_is_not_stored_in_plain_text(self):
        self.application.refresh_from_db()
        self.assertNotEqual(self.application.client_secret, self.secret)

    def test_token_endpoint_is_rate_limited(self):
        with patch.dict(SimpleRateThrottle.THROTTLE_RATES, {"auth_minute": "2/min"}):
            statuses = [self._token(secret="wrong").status_code for _ in range(4)]

        self.assertEqual(statuses[:2], [401, 401])
        self.assertEqual(statuses[2:], [429, 429])

    # ---------- using a token ----------
    def test_bearer_token_reaches_the_api(self):
        response = self._get(self._bearer())
        self.assertEqual(response.status_code, 200)

    def test_request_without_a_token_is_refused(self):
        self.assertIn(self._get({}).status_code, (401, 403))

    def test_garbage_token_is_refused(self):
        response = self._get({"HTTP_AUTHORIZATION": "Bearer not-a-real-token"})
        self.assertIn(response.status_code, (401, 403))

    def test_token_acts_as_the_applications_service_user(self):
        request = APIRequestFactory().get(READ_URL, **self._bearer())

        user, token = NearBeachOAuth2Authentication().authenticate(Request(request))

        self.assertEqual(user, self.service_user)
        self.assertEqual(token.application, self.application)

    def test_service_user_with_no_group_gets_no_access(self):
        UserGroup.objects.filter(username=self.service_user).delete()
        response = self._get(self._bearer(), WRITE_URL)
        self.assertIn(response.status_code, (401, 403))

    def test_expired_token_is_refused(self):
        headers = self._bearer()
        AccessToken.objects.update(expires=timezone.now() - timedelta(seconds=1))

        self.assertIn(self._get(headers).status_code, (401, 403))

    def test_revoked_token_is_refused(self):
        token = self._token().json()["access_token"]
        revoke = self.client.post(
            "/o/revoke_token/",
            {"token": token, "client_id": self.application.client_id, "client_secret": self.secret},
        )
        self.assertEqual(revoke.status_code, 200)

        self.assertIn(self._get({"HTTP_AUTHORIZATION": f"Bearer {token}"}).status_code, (401, 403))

    def test_disabled_service_user_is_refused(self):
        headers = self._bearer()
        self.service_user.is_active = False
        self.service_user.save()

        self.assertIn(self._get(headers).status_code, (401, 403))

    def test_application_with_no_service_user_is_refused(self):
        headers = self._bearer()
        Application.objects.filter(pk=self.application.pk).update(user=None)

        self.assertIn(self._get(headers).status_code, (401, 403))

    # ---------- scopes ----------
    def test_read_token_cannot_make_changes(self):
        response = APIClient().post(WRITE_URL, {}, format="json", **self._bearer("read"))

        self.assertEqual(response.status_code, 403)
        self.assertIn(SCOPE_MESSAGE, response.json()["detail"])

    def test_write_token_is_not_stopped_by_scope(self):
        # Whether the create then succeeds is the view's business - it just must not be the scope check saying no
        response = APIClient().post(WRITE_URL, {}, format="json", **self._bearer("read write"))

        self.assertNotIn(SCOPE_MESSAGE, str(response.content))

    def test_scope_permission(self):
        cases = {
            ("GET", "read"): True,
            ("GET", "write"): True,
            ("GET", ""): False,
            ("HEAD", "read"): True,
            ("POST", "read"): False,
            ("PATCH", "read"): False,
            ("DELETE", "read"): False,
            ("POST", "write"): True,
            ("DELETE", "read write"): True,
        }
        for (method, scope), expected in cases.items():
            with self.subTest(method=method, scope=scope):
                token = AccessToken(scope=scope, expires=timezone.now() + timedelta(hours=1))
                request = Request(APIRequestFactory().generic(method, "/"))
                request.auth = token

                self.assertEqual(OAuth2ScopePermission().has_permission(request, None), expected)

    # ---------- the other ways in still work ----------
    def test_session_login_is_not_limited_by_scopes(self):
        self.client.post(
            "/api/v1/authentication/",
            {"username": "admin", "password": "Test1234$", "otp_token": ""},
            format="json",
        )
        response = self.client.post(WRITE_URL, {}, format="json")
        self.assertNotIn(SCOPE_MESSAGE, str(response.content))

    def test_knox_token_still_works(self):
        _, token = ExtendsAuthToken.objects.create(user=self.service_user, change_user=self.service_user)
        response = APIClient().get(READ_URL, HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(response.status_code, 200)

    # ---------- what is exposed ----------
    def test_application_management_pages_are_not_exposed(self):
        for name in ("list", "register", "detail"):
            with self.subTest(name):
                with self.assertRaises(NoReverseMatch):
                    reverse(f"oauth2_provider:{name}")

    def test_oauth2_security_scheme_is_in_the_openapi_schema(self):
        self.client.post(
            "/api/v1/authentication/",
            {"username": "admin", "password": "Test1234$", "otp_token": ""},
            format="json",
        )
        schema = self.client.get("/api/v1/schema/?format=json").json()

        flows = schema["components"]["securitySchemes"]["oauth2"]["flows"]
        self.assertEqual(flows["clientCredentials"]["tokenUrl"], "/o/token/")
        self.assertEqual(flows["authorizationCode"]["authorizationUrl"], "/o/authorize/")
        self.assertEqual(set(flows["clientCredentials"]["scopes"]), {"read", "write"})


class OAuth2AuthorizationCodeTests(BaseApiClass):
    """The authorization code flow, for apps acting on behalf of a person who signs in to NearBeach"""

    REDIRECT = "https://app.example.com/callback"

    def setUp(self):
        super().setUp()
        cache.clear()
        self.user = User.objects.get(username="team_member")
        self.application = Application.objects.create(
            name="Mobile app",
            user=self.user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris=self.REDIRECT,
            skip_authorization=False,
        )
        self.verifier = "v" * 64
        self.challenge = base64.urlsafe_b64encode(hashlib.sha256(self.verifier.encode()).digest()).rstrip(b"=").decode()

    def _authorize_params(self, **overrides):
        params = {
            "response_type": "code",
            "client_id": self.application.client_id,
            "redirect_uri": self.REDIRECT,
            "scope": "read",
            "state": "xyz",
            "code_challenge": self.challenge,
            "code_challenge_method": "S256",
        }
        params.update(overrides)
        return params

    def _sign_in(self):
        self.client.post(
            "/api/v1/authentication/",
            {"username": "team_member", "password": "Test1234$", "otp_token": ""},
            format="json",
        )

    def _approve(self, **overrides):
        return self.client.post("/o/authorize/", {**self._authorize_params(**overrides), "allow": "Allow"})

    def test_signed_out_user_is_sent_to_the_login_page(self):
        response = self.client.get("/o/authorize/", self._authorize_params())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/?next="))

    def test_full_flow_gives_a_token_that_acts_as_the_person(self):
        self._sign_in()
        approved = self._approve()
        self.assertEqual(approved.status_code, 302)
        query = parse_qs(urlparse(approved.url).query)
        self.assertEqual(query["state"], ["xyz"])

        token_response = APIClient().post(TOKEN_URL, {
            "grant_type": "authorization_code",
            "code": query["code"][0],
            "redirect_uri": self.REDIRECT,
            "client_id": self.application.client_id,
            "code_verifier": self.verifier,
        })
        self.assertEqual(token_response.status_code, 200, token_response.content)
        body = token_response.json()
        self.assertIn("refresh_token", body)

        api = APIClient().get(READ_URL, HTTP_AUTHORIZATION=f"Bearer {body['access_token']}")
        self.assertEqual(api.status_code, 200)
        self.assertEqual(AccessToken.objects.get().user, self.user)

    def test_pkce_is_required(self):
        self._sign_in()
        params = self._authorize_params()
        del params["code_challenge"], params["code_challenge_method"]

        response = self.client.get("/o/authorize/", params)

        self.assertNotEqual(response.status_code, 200)

    def test_wrong_pkce_verifier_gets_no_token(self):
        self._sign_in()
        query = parse_qs(urlparse(self._approve().url).query)

        response = APIClient().post(TOKEN_URL, {
            "grant_type": "authorization_code",
            "code": query["code"][0],
            "redirect_uri": self.REDIRECT,
            "client_id": self.application.client_id,
            "code_verifier": "w" * 64,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(AccessToken.objects.count(), 0)

    def test_unregistered_redirect_uri_is_refused(self):
        self._sign_in()
        response = self.client.get("/o/authorize/", self._authorize_params(redirect_uri="https://evil.example.com/cb"))
        self.assertEqual(response.status_code, 400)

    def test_refresh_token_rotates(self):
        self._sign_in()
        query = parse_qs(urlparse(self._approve().url).query)
        first = APIClient().post(TOKEN_URL, {
            "grant_type": "authorization_code",
            "code": query["code"][0],
            "redirect_uri": self.REDIRECT,
            "client_id": self.application.client_id,
            "code_verifier": self.verifier,
        }).json()

        refreshed = APIClient().post(TOKEN_URL, {
            "grant_type": "refresh_token",
            "refresh_token": first["refresh_token"],
            "client_id": self.application.client_id,
        })

        self.assertEqual(refreshed.status_code, 200, refreshed.content)
        self.assertNotEqual(refreshed.json()["refresh_token"], first["refresh_token"])

        # The old refresh token is spent
        reused = APIClient().post(TOKEN_URL, {
            "grant_type": "refresh_token",
            "refresh_token": first["refresh_token"],
            "client_id": self.application.client_id,
        })
        self.assertEqual(reused.status_code, 400)
