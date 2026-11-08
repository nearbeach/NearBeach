from oauth2_provider.models import get_access_token_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

READ_SCOPE = "read"
WRITE_SCOPE = "write"


class OAuth2ScopePermission(BasePermission):
    """Narrows what an OAuth2 token may do - `read` for safe methods, `write` for the rest

    Scopes only ever take rights away: the user behind the token still needs their group permissions. Requests that
    do not use an OAuth2 token (session, basic, Knox) are not affected.
    """

    message = "The OAuth2 token does not have the scope this request needs."

    def has_permission(self, request, view) -> bool:
        if not isinstance(request.auth, get_access_token_model()):
            return True

        granted = set(request.auth.scope.split())
        if request.method in SAFE_METHODS:
            return bool(granted & {READ_SCOPE, WRITE_SCOPE})

        return WRITE_SCOPE in granted
