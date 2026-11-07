import time
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from joserfc import jwt
from joserfc.jwk import KeySet, RSAKey

from NearBeach.models.authentication.oidc_provider import OidcIdentity, OidcProvider
from NearBeach.services.OidcService import OidcService
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

HOST = "https://keycloak.example.com"
ISSUER = f"{HOST}/realms/nearbeach"
CLIENT_ID = "nearbeach"
USERNAME = "team_member"


def keycloak_discovery(issuer=ISSUER):
    """The parts of a Keycloak realm's discovery document NearBeach reads, shaped as Keycloak serves them"""
    return {
        "issuer": issuer,
        "authorization_endpoint": f"{issuer}/protocol/openid-connect/auth",
        "token_endpoint": f"{issuer}/protocol/openid-connect/token",
        "jwks_uri": f"{issuer}/protocol/openid-connect/certs",
        "userinfo_endpoint": f"{issuer}/protocol/openid-connect/userinfo",
        "id_token_signing_alg_values_supported": ["RS256", "ES256"],
        "code_challenge_methods_supported": ["plain", "S256"],
    }


class KeycloakOidcTests(BaseApiClass):
    """Tests using the shapes Keycloak really sends

    Notes
    ~~~~~
    - Keycloak puts the realm in the issuer, signs with RS256 and publishes several keys (a signing key and an
      encryption key), identified by `kid`
    - Its ID tokens carry `azp` (the client), and `aud` is often a *list* when the realm has extra audiences
    - Realm roles live in `realm_access`, which NearBeach must ignore rather than trip over
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signing_key = RSAKey.generate_key(2048, parameters={"kid": "keycloak-sig", "use": "sig", "alg": "RS256"})
        cls.encryption_key = RSAKey.generate_key(2048, parameters={"kid": "keycloak-enc", "use": "enc", "alg": "RSA-OAEP"})

    def setUp(self):
        super().setUp()
        cache.clear()
        self.discovery = keycloak_discovery()
        self.fetched_urls = []

        self.provider = OidcProvider.objects.create(
            name="Keycloak",
            slug="keycloak",
            issuer_url=ISSUER,
            client_id=CLIENT_ID,
            client_secret="secret",
        )
        user = User.objects.get(username=USERNAME)
        OidcIdentity.objects.create(user=user, provider=self.provider, subject="kc-sub-1", change_user=user)
        self.user = user

        for view in ("OidcLoginView", "OidcCallbackView"):
            patcher = patch(f"NearBeach.views.api_v1.authentication.oidc_api_view.{view}.throttle_classes", [])
            patcher.start()
            self.addCleanup(patcher.stop)

        patcher = patch("NearBeach.services.OidcService.OidcService._get_json", side_effect=self._get_json)
        patcher.start()
        self.addCleanup(patcher.stop)

    # ---------- helpers ----------
    def _get_json(self, url):
        self.fetched_urls.append(url)
        if url.endswith("/openid-configuration"):
            return self.discovery
        return KeySet([self.signing_key, self.encryption_key]).as_dict(private=False)

    def _claims(self, **overrides):
        claims = {
            "iss": ISSUER,
            "aud": CLIENT_ID,
            "azp": CLIENT_ID,
            "sub": "kc-sub-1",
            "typ": "ID",
            "exp": int(time.time()) + 300,
            "iat": int(time.time()),
            "auth_time": int(time.time()),
            "session_state": "11111111-2222-3333-4444-555555555555",
            "email_verified": True,
            "preferred_username": "team_member",
            "email": "team_member@example.com",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
        }
        claims.update(overrides)
        return claims

    def _sign(self, claims, key=None, header=None):
        return jwt.encode(header or {"alg": "RS256", "typ": "JWT", "kid": "keycloak-sig"}, claims, key or self.signing_key)

    def _sign_in(self, **claim_overrides):
        """Run the flow with a Keycloak-shaped token; returns the callback response"""
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        token = self._sign(self._claims(nonce=flow["nonce"], **claim_overrides))
        return self._callback(flow, token)

    def _callback(self, flow, token):
        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"id_token": token, "access_token": "ignored", "token_type": "Bearer"},
        ):
            return self.client.get(
                "/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": flow["state"]}
            )

    def _assert_signed_in(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))

    def _assert_refused(self, response, code="invalid_id_token"):
        self.assertEqual(response.url, f"/login/?sso_error={code}")
        self.assertNotIn("_auth_user_id", self.client.session)

    # ---------- discovery ----------
    def test_discovery_url_is_built_from_the_realm_issuer(self):
        self._sign_in()
        self.assertEqual(self.fetched_urls[0], f"{ISSUER}/.well-known/openid-configuration")
        self.assertEqual(self.fetched_urls[1], f"{ISSUER}/protocol/openid-connect/certs")

    def test_trailing_slash_on_the_configured_issuer_still_works(self):
        self.provider.issuer_url = f"{ISSUER}/"
        self.provider.save()

        self._assert_signed_in(self._sign_in())
        self.assertEqual(self.fetched_urls[0], f"{ISSUER}/.well-known/openid-configuration")

    def test_discovery_is_cached_between_sign_ins(self):
        self._sign_in()
        self.client.logout()
        self._sign_in()

        discovery_fetches = [url for url in self.fetched_urls if url.endswith("/openid-configuration")]
        self.assertEqual(len(discovery_fetches), 1)

    def test_discovery_for_a_different_realm_is_refused(self):
        # e.g. the issuer typed with the wrong realm, or a hijacked/misrouted host
        self.discovery = keycloak_discovery(f"{HOST}/realms/another-realm")

        response = self.client.get("/api/v1/authentication/oidc/keycloak/login/")

        self.assertEqual(response.url, "/login/?sso_error=provider_misconfigured")

    def test_authorization_request_uses_the_keycloak_endpoint_and_scopes(self):
        response = self.client.get("/api/v1/authentication/oidc/keycloak/login/")

        self.assertTrue(response.url.startswith(f"{ISSUER}/protocol/openid-connect/auth?"))
        self.assertIn("scope=openid+email+profile", response.url)
        self.assertIn(f"redirect_uri=http%3A%2F%2Ftestserver%2Fapi%2Fv1%2Fauthentication%2Foidc%2Fkeycloak%2Fcallback%2F", response.url)

    # ---------- the ID token as Keycloak sends it ----------
    def test_full_keycloak_token_signs_the_user_in(self):
        self._assert_signed_in(self._sign_in())

    def test_audience_list_containing_the_client_is_accepted(self):
        self._assert_signed_in(self._sign_in(aud=[CLIENT_ID, "account"]))

    def test_audience_list_without_the_client_is_refused(self):
        self._assert_refused(self._sign_in(aud=["account", "broker"]))

    def test_realm_roles_do_not_affect_sign_in(self):
        self._assert_signed_in(self._sign_in(realm_access={"roles": ["admin"]}, resource_access={"x": {"roles": []}}))

    # ---------- tokens Keycloak would never send, but an attacker might ----------
    def test_unsigned_token_is_refused(self):
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        header = {"alg": "none", "typ": "JWT"}
        import base64, json

        def b64(data):
            return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()

        unsigned = f"{b64(header)}.{b64(self._claims(nonce=flow['nonce']))}."

        self._assert_refused(self._callback(flow, unsigned))

    def test_token_signed_with_hmac_using_the_public_key_is_refused(self):
        # Classic algorithm-confusion attack: HS256 signed with the (public) RSA key material as the secret.
        # joserfc refuses to build this token, so it is assembled by hand
        import base64, hashlib, hmac, json

        def b64(raw):
            return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        signing_input = ".".join([
            b64(json.dumps({"alg": "HS256", "kid": "keycloak-sig"}).encode()),
            b64(json.dumps(self._claims(nonce=flow["nonce"])).encode()),
        ])
        signature = hmac.new(self.signing_key.as_pem(private=False), signing_input.encode(), hashlib.sha256).digest()

        self._assert_refused(self._callback(flow, f"{signing_input}.{b64(signature)}"))

    def test_token_from_a_kid_the_realm_does_not_publish_is_refused(self):
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        rogue = RSAKey.generate_key(2048, parameters={"kid": "rogue"})
        token = self._sign(self._claims(nonce=flow["nonce"]), key=rogue, header={"alg": "RS256", "kid": "rogue"})

        self._assert_refused(self._callback(flow, token))

    def test_token_without_a_subject_is_refused(self):
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        claims = self._claims(nonce=flow["nonce"])
        del claims["sub"]

        self._assert_refused(self._callback(flow, self._sign(claims)))

    def test_response_without_an_id_token_is_refused(self):
        # Happens when the client was set up without the `openid` scope
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"access_token": "only-an-access-token"},
        ):
            response = self.client.get(
                "/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": flow["state"]}
            )
        self._assert_refused(response, "missing_id_token")

    def test_token_just_past_expiry_is_inside_the_clock_leeway(self):
        self._assert_signed_in(self._sign_in(exp=int(time.time()) - 30))

    def test_token_well_past_expiry_is_refused(self):
        self._assert_refused(self._sign_in(exp=int(time.time()) - 600))

    # ---------- client types ----------
    def test_public_client_sends_no_secret(self):
        self.provider.client_secret = ""
        self.provider.save()

        session = OidcService(self.provider, "http://testserver/cb")._session()

        self.assertEqual(session.token_endpoint_auth_method, "none")

    def test_confidential_client_posts_its_secret(self):
        session = OidcService(self.provider, "http://testserver/cb")._session()

        self.assertEqual(session.token_endpoint_auth_method, "client_secret_post")

    def test_token_request_carries_the_pkce_verifier(self):
        self.client.get("/api/v1/authentication/oidc/keycloak/login/")
        flow = self.client.session["oidc_flow"]
        token = self._sign(self._claims(nonce=flow["nonce"]))

        with patch(
            "authlib.integrations.requests_client.OAuth2Session.fetch_token",
            return_value={"id_token": token},
        ) as fetch_token:
            self.client.get("/api/v1/authentication/oidc/keycloak/callback/", {"code": "abc", "state": flow["state"]})

        self.assertEqual(fetch_token.call_args.kwargs["code_verifier"], flow["code_verifier"])
        self.assertEqual(fetch_token.call_args.kwargs["code"], "abc")
        self.assertEqual(fetch_token.call_args.args[0], f"{ISSUER}/protocol/openid-connect/token")

    # ---------- Keycloak specific user data ----------
    def test_keycloak_user_without_a_verified_email_is_still_matched_by_subject(self):
        self._assert_signed_in(self._sign_in(email_verified=False))
