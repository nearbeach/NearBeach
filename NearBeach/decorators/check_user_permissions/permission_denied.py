from django.core.exceptions import PermissionDenied
from functools import wraps


def check_permission_denied():
    """Just a test function - don't worry about it"""

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator

