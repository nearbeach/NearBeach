from django.core.exceptions import PermissionDenied
from functools import wraps
from .partials.generic_permissions import generic_permissions


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
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Extract the url string, and split into a list
            url_string = request.request.path
            url_list = url_string.replace("/api/v0/", "").removesuffix("/").split("/")

            destination = ""
            if len(url_list) == 1:
                destination = url_list[0]
            elif len(url_list) == 2:
                destination = url_list[0]
                kwargs["location_id"] = url_list[1]

            passes, user_level, extra_level = generic_permissions(request, destination, kwargs)

            if not passes:
                raise PermissionDenied

            if user_level >= min_permission_level or extra_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_object_data_api_permissions():
    return None