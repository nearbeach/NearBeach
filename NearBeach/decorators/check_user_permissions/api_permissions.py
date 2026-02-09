from django.core.exceptions import PermissionDenied
from functools import wraps

# TODO - generic, get destination from url
# TODO - determine if it is an object, or child object and apply appropriate permission check
def check_user_api_permissions(min_permission_level):
    """
    Checks the user's generic permissions. It will gather both the
    - destination
    - location id
    from the API Url.
    From here it will determine which partial permission it should
    be checking against. The result from the partial will determine
    if the user is granted permission or denied.
    """
    return True
