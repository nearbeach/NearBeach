from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Max
from functools import wraps

from NearBeach.models import *


def project_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                return func(request, *args, **kwargs)

            # Default user level is 0
            user_group_results = user_group.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing the project_id through, we will use a different function
            if len(kwargs) > 0:
                # Check user permissions AGAINST the project and it's groups
                project_instance = project.objects.get(project_id=kwargs['project_id'])

                # Determine if there are any cross over with user groups and project groups
                group_results = group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The project groups
                        group_id__in=object_assignment.objects.filter(
                            is_deleted=False,
                            project_id=kwargs['project_id'],
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
                Max('permission_set__project')
            )['permission_set__project__max']

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator
