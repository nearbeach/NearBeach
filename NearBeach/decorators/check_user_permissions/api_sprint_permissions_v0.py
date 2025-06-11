from django.core.exceptions import PermissionDenied
from functools import wraps
from rest_framework import status
from rest_framework.response import Response

from NearBeach.models import Sprint

from NearBeach.decorators.check_user_permissions.object_permissions import FUNCTION_DICT
from NearBeach.serializers.sprint_serializer import SprintSerializer


def check_api_sprint_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            _request = request.request if hasattr(request, "request") else request

            serializer = SprintSerializer(data=_request.data, context={'request': _request})
            if not serializer.is_valid():
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # If user is admin - grant them all permissions
            if _request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Flat pack values
            destination = serializer.data.get("destination")
            location_id = serializer.data.get("location_id")

            # Fold the location id into the {destination}_id.
            kwargs[F"{destination}_id"] = location_id


            # User the FUNCTION_DICT to determine which partial permissions we need
            # to reference
            passes, user_level, _ = FUNCTION_DICT[destination](_request, kwargs)

            if not passes:
                raise PermissionDenied

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner
    return decorator
