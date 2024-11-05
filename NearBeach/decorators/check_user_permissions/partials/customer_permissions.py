from django.db.models import Max
from NearBeach.models import UserGroup


def customer_permissions(request, *args, **kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__customer")
    )["permission_set__customer__max"]

    return True, user_level, False
