import logging

from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import constant_time_compare
from django.utils.http import url_has_allowed_host_and_scheme
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from NearBeach.models.authentication.oidc_provider import OidcProvider
from NearBeach.serializers.authentication.oidc_provider_serializer import OidcProviderSerializer
from NearBeach.services.OidcService import OidcError, OidcService
from NearBeach.services.OidcUserService import OidcUserService
from NearBeach.utils.throttle.AuthHourThrottle import AuthHourThrottle
from NearBeach.utils.throttle.AuthMinuteThrottle import AuthMinuteThrottle

logger = logging.getLogger(__name__)

SESSION_KEY = "oidc_flow"


def _enabled_providers():
    return OidcProvider.objects.filter(is_enabled=True, is_deleted=False)


def _redirect_uri(request, provider: OidcProvider) -> str:
    return request.build_absolute_uri(reverse("oidc-callback", kwargs={"slug": provider.slug}))


def _login_error(code: str) -> HttpResponseRedirect:
    return HttpResponseRedirect(f"/login/?{OidcService.error_query(code)}")


class OidcProvidersView(APIView):
    """Lists the single sign-on providers the login page should offer"""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = []  # Public, read-only, and loaded on every visit to the login page
    serializer_class = OidcProviderSerializer

    @extend_schema(responses=OidcProviderSerializer(many=True))
    def get(self, request):
        providers = [
            {
                "name": provider.name,
                "slug": provider.slug,
                "login_url": reverse("oidc-login", kwargs={"slug": provider.slug}),
            }
            for provider in _enabled_providers().order_by("name")
        ]
        return Response(OidcProviderSerializer(providers, many=True).data)


@extend_schema(exclude=True)
class OidcLoginView(APIView):
    """Sends the browser to the identity provider"""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [AuthMinuteThrottle, AuthHourThrottle]

    def get(self, request, slug):
        provider = get_object_or_404(_enabled_providers(), slug=slug)

        try:
            flow = OidcService(provider, _redirect_uri(request, provider)).start()
        except OidcError as error:
            logger.warning("OIDC login for %s failed to start: %s", slug, error)
            return _login_error(error.code)

        next_url = request.GET.get("next", "/")
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            next_url = "/"

        request.session[SESSION_KEY] = {
            "slug": slug,
            "state": flow.state,
            "nonce": flow.nonce,
            "code_verifier": flow.code_verifier,
            "next": next_url,
        }
        return HttpResponseRedirect(flow.url)


@extend_schema(exclude=True)
class OidcCallbackView(APIView):
    """Where the identity provider sends the browser back to"""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [AuthMinuteThrottle, AuthHourThrottle]

    def get(self, request, slug):
        provider = get_object_or_404(_enabled_providers(), slug=slug)

        # One go per flow - whatever happens next, this state is spent
        flow = request.session.pop(SESSION_KEY, None)
        if not flow or flow.get("slug") != slug:
            return _login_error("invalid_state")

        if "error" in request.GET:
            return _login_error("provider_denied")

        code = request.GET.get("code", "")
        if not code or not constant_time_compare(request.GET.get("state", ""), flow["state"]):
            return _login_error("invalid_state")

        try:
            claims = OidcService(provider, _redirect_uri(request, provider)).finish(
                code=code,
                code_verifier=flow["code_verifier"],
                nonce=flow["nonce"],
            )
            user = OidcUserService(provider).resolve(claims)
        except OidcError as error:
            logger.warning("OIDC login for %s failed: %s", slug, error)
            return _login_error(error.code)

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return HttpResponseRedirect(flow["next"])
