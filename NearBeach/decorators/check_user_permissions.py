from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Max
from functools import wraps

from NearBeach.models import *

def check_user_customer_permissions(min_permission_level):
    #Function is only used when checking user permissions against customers - as they are different
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            #if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = user_group.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max('permission_set__customer')
            )['permission_set__customer__max']

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator


def check_user_kanban_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, kanban_card_id, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = user_group.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Determine if there are any cross over with user groups and object_lookup groups
            group_results = group.objects.filter(
                Q(
                    is_deleted=False,
                    # The object_lookup groups
                    group_id__in=object_assignment.objects.filter(
                        is_deleted=False,
                        kanban_board_id__in=kanban_card.objects.filter(
                            kanban_card_id=kanban_card_id,
                        ).values('kanban_board_id')
                    ).values('group_id'),
                ) &
                Q(
                    group_id__in=user_group_results.values('group_id')
                )
            )

            # Check to make sure the user groups intersect
            if len(group_results) == 0:
                # There are no matching groups - i.e. the user does not have any permission
                raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max('permission_set__kanban_board')
            )['permission_set__kanban_board__max']

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, kanban_card_id, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator


def check_user_permissions(min_permission_level, object_lookup=''):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = user_group.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing the object_lookup through, we will use a different function
            if len(kwargs) > 0:
                # Determine if there are any cross over with user groups and object_lookup groups
                group_results = group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The object_lookup groups
                        group_id__in=object_assignment.objects.filter(
                            is_deleted=False,
                            **{object_lookup: kwargs[object_lookup]},
                        ).values('group_id'),
                    ) &
                    Q(
                        group_id__in=user_group_results.values('group_id')
                    )
                )

                # Check to make sure the user groups intersect
                if len(group_results) == 0:
                    # There are no matching groups - i.e. the user does not have any permission
                    raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max('permission_set__%s' % object_lookup.replace('_id',''))
            )['permission_set__%s__max' % object_lookup.replace('_id','')]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator


def check_user_requirement_item_permissions(min_permission_level):
    #Function is only used when checking user permissions against customers - as they are different
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            #if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Get the requirement_item instance
            requirement_item_results = requirement_item.objects.get(
                **{'requirement_item_id': kwargs['requirement_item_id']},
            )

            # Get the requirement instance
            requirement_results = requirement.objects.get(
                requirement_id=requirement_item_results.requirement_id,
            )
            
            # Get the requirement groups
            user_group_results = user_group.objects.filter(
                Q (
                    is_deleted=False,
                    group_id__in=object_assignment.objects.filter(
                        is_deleted=False,
                        group_id__isnull=False,
                        requirement_id=requirement_results.requirement_id,
                    ).values('group_id'),
                ) &
                Q (
                    username=request.user,
                )
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max('permission_set__requirement')
            )['permission_set__requirement__max']

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator


def check_rfc_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = user_group.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing the object_lookup through, we will use a different function
            if len(kwargs) > 0:
                # Determine if there are any cross over with user groups and object_lookup groups
                group_results = group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The object_lookup groups
                        group_id__in=object_assignment.objects.filter(
                            is_deleted=False,
                            # **{object_lookup: kwargs[object_lookup]},
                            request_for_change_id = kwargs['rfc_id'],
                        ).values('group_id'),
                    ) &
                    Q(
                        group_id__in=user_group_results.values('group_id')
                    )
                )

                # Check to make sure the user groups intersect
                if len(group_results) == 0:
                    # There are no matching groups - i.e. the user does not have any permission
                    raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max('permission_set__request_for_change')
            )['permission_set__request_for_change__max']

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator
