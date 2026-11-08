"""Bearer token authentication for the API, using tokens issued by NearBeach's own OAuth2 provider"""

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.exceptions import AuthenticationFailed


class NearBeachOAuth2Authentication(OAuth2Authentication):
    """OAuth2Authentication that also works for machine-to-machine (client credentials) tokens

    A client credentials token belongs to an application, not a person, so django-oauth-toolkit stores it with no
    user. NearBeach's permissions are all group based, so such a token acts as the application's owner - a service
    user that an administrator has put in the groups the integration needs.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, token = result
        if user is None:
            user = token.application.user if token.application else None

        # Fail closed: a token with nobody behind it must never reach a view as anonymous
        if user is None:
            raise AuthenticationFailed("This OAuth2 application has no service user.")
        if not user.is_active:
            raise AuthenticationFailed("The user behind this token is disabled.")

        return user, token
