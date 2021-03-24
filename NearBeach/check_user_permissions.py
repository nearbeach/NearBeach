from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

# def project_permissions(func=None):
#     def func_wrapper(request, *args, **kwargs):
#         return func(request, *args, **kwargs)
#
#         # Does not pass - permission denied
#         # raise PermissionDenied
#
#     return func_wrapper


def project_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user_level = 1
            if user_level >= min_permission_level:
                return func(request, *args, **kwargs)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator
