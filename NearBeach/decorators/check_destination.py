from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Max
from functools import wraps

OBJECT_ARRAY = [
    'customer',
    'kanban',
    'kanban_board',
    'kanban_card',
    'requirement',
    'requirement_item',
    'request_for_change',
    'organisation',
    'project',
    'task',
]


def check_destination():
    def decorator(func):
        @wraps(func)
        def inner(request, destination, *args, **kwargs):
            # See if the destination is correct (permission denied if not).
            if not destination in OBJECT_ARRAY:
                raise PermissionDenied

            # It passed - return the function
            return func(request, destination, *args, **kwargs)
        return inner
    return decorator
