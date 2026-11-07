"""Service handling the OpenID Connect authorization-code flow (with PKCE) against a configured provider"""

import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import requests
from authlib.common.security import generate_token
from authlib.integrations.requests_client import OAuth2Session
from django.core.cache import cache
from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import KeySet

from NearBeach.models.authentication.oidc_provider import OidcProvider

REQUEST_TIMEOUT_SECONDS = 10
METADATA_CACHE_SECONDS = 3600
CLOCK_LEEWAY_SECONDS = 60
ID_TOKEN_ALGORITHMS = ["RS256", "RS384", "RS512", "PS256", "PS384", "PS512", "ES256", "ES384", "ES512", "EdDSA"]


class OidcError(Exception):
    """Raised when a sign in fails. The code is safe to show the user, the detail is not"""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code


@dataclass
class OidcAuthorizationRequest:
    """Everything we have to remember between sending the user away and them coming back"""

    url: str
    state: str
    nonce: str
    code_verifier: str


class OidcService:
    """Class talking to the identity provider on behalf of a single OidcProvider"""

    def __init__(self, provider: OidcProvider, redirect_uri: str) -> None:
        self.provider = provider
        self.redirect_uri = redirect_uri

    @staticmethod
    def _get_json(url: str) -> dict:
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as error:
            raise OidcError("provider_unavailable", str(error)) from error

    def _metadata(self) -> dict:
        """The provider's discovery document - cached, as it hardly ever changes"""
        cache_key = f"oidc_metadata_{self.provider.pk}_{self.provider.issuer_url}"
        metadata = cache.get(cache_key)
        if metadata is None:
            metadata = self._get_json(
                f"{self.provider.issuer_url.rstrip('/')}/.well-known/openid-configuration"
            )
            if self._normalise(metadata.get("issuer")) != self._normalise(self.provider.issuer_url):
                raise OidcError("provider_misconfigured", "Discovery issuer does not match the configured issuer")
            cache.set(cache_key, metadata, METADATA_CACHE_SECONDS)
        return metadata

    @staticmethod
    def _normalise(url) -> str:
        return str(url or "").rstrip("/")

    def _session(self) -> OAuth2Session:
        return OAuth2Session(
            client_id=self.provider.client_id,
            client_secret=self.provider.client_secret or None,
            scope=self.provider.scopes,
            redirect_uri=self.redirect_uri,
            code_challenge_method="S256",
            token_endpoint_auth_method="client_secret_post" if self.provider.client_secret else "none",
        )

    def start(self) -> OidcAuthorizationRequest:
        """Build the URL we send the user to, plus the values we need to check when they return"""
        state = secrets.token_urlsafe(32)
        nonce = secrets.token_urlsafe(32)
        code_verifier = generate_token(64)

        url, _ = self._session().create_authorization_url(
            self._metadata()["authorization_endpoint"],
            state=state,
            nonce=nonce,
            code_verifier=code_verifier,
        )
        return OidcAuthorizationRequest(url=url, state=state, nonce=nonce, code_verifier=code_verifier)

    def finish(self, code: str, code_verifier: str, nonce: str) -> dict:
        """Swap the code for tokens and return the verified claims from the ID token"""
        metadata = self._metadata()
        try:
            token = self._session().fetch_token(
                metadata["token_endpoint"],
                grant_type="authorization_code",
                code=code,
                code_verifier=code_verifier,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except Exception as error:  # authlib raises several types for a rejected code
            raise OidcError("token_exchange_failed", str(error)) from error

        id_token = token.get("id_token")
        if not id_token:
            raise OidcError("missing_id_token")

        return self._verify_id_token(id_token, metadata, nonce)

    def _verify_id_token(self, id_token: str, metadata: dict, nonce: str) -> dict:
        keys = KeySet.import_key_set(self._get_json(metadata["jwks_uri"]))
        try:
            decoded = jwt.decode(id_token, keys, algorithms=ID_TOKEN_ALGORITHMS)
            jwt.JWTClaimsRegistry(
                leeway=CLOCK_LEEWAY_SECONDS,
                iss={"essential": True, "value": metadata["issuer"]},
                aud={"essential": True, "value": self.provider.client_id},
                sub={"essential": True},
                exp={"essential": True},
                nonce={"essential": True, "value": nonce},
            ).validate(decoded.claims)
        except (JoseError, ValueError) as error:
            raise OidcError("invalid_id_token", str(error)) from error

        return decoded.claims

    @staticmethod
    def error_query(code: str) -> str:
        """Query string the login page reads to show the user what went wrong"""
        return urlencode({"sso_error": code})
