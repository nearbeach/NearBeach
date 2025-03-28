from django.core.exceptions import PermissionDenied
from functools import wraps
from .partials.generic_permissions import generic_permissions
from NearBeach.serializers.destination_serializer import DestinationSerializer
from rest_framework import status
from rest_framework.response import Response


def api_object_data_permissions(min_permission_level):
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
            serializer = DestinationSerializer(data=request.request.data)
            if not serializer.is_valid():
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            destination = serializer.data["destination"]
            kwargs["location_id"] = serializer.data["location_id"]

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