from django.core.exceptions import PermissionDenied
from functools import wraps
from django.db.models import Max
from NearBeach.models import UserGroup, ObjectTemplateGroup, ScheduledObject


def check_schedule_object_permissions(min_permission_level):
    """
    Checks the user's permissions for the schedule object functionality in NearBeach.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Get permission sets
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Get the scheduled object id if it exists
            scheduled_object_id = kwargs.get('schedule_object_id', None)
            if scheduled_object_id is not None:
                user_group_results = user_group_results.filter(
                    group_id__in=ObjectTemplateGroup.objects.filter(
                        is_deleted=False,
                        object_template_id__in=ScheduledObject.objects.filter(
                            is_deleted=False,
                            schedule_object_id=scheduled_object_id,
                        ).values("object_template_id")
                    ).values("group_id")
                )

            if len(user_group_results) > 0:
                # Get the max permission value from user_group_results
                user_level = user_group_results.aggregate(
                    Max("permission_set__schedule_object")
                )["permission_set__schedule_object__max"]

                if user_level >= min_permission_level:
                    # Everything is fine - continue on
                    return func(request, *args, **kwargs, user_level=user_level)

            raise PermissionDenied
        return inner
    return decorator
