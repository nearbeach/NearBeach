# from django.core.exceptions import PermissionDenied
# from django.db.models import Q, Max
# from functools import wraps
#
# from NearBeach.models import (
#     UserGroup,
#     Group,
#     ObjectAssignment,
#     KanbanCard,
#     PermissionSet,
#     RequirementItem,
#     Requirement,
#     ChangeTask,
# )
#
#
# def check_change_task_permissions(min_permission_level):
#     """Check the user's ability to interact with change tasks via the RFC"""
#     def decorator(func):
#         @wraps(func)
#         def inner(request, *args, **kwargs):
#             # If user is admin - grant them all permission
#             if request.user.is_superuser:
#                 # Return the function with a user_level of 4
#                 return func(request, *args, **kwargs, user_level=4)
#
#             # Checks the user permissions
#             passes, user_level = object_change_task(request, kwargs)
#
#             if not passes:
#                 raise PermissionDenied
#
#             if user_level >= min_permission_level:
#                 # Everything is fine - continue on
#                 return func(request, *args, **kwargs, user_level=user_level)
#
#             # Does not meet conditions
#             raise PermissionDenied
#
#         return inner
#
#     return decorator
#
#
#
#
# def check_user_kanban_permissions(min_permission_level):
#     """
#     Checks the user permissions for the kanban board. It returns the user's permission
#     levels, unless they have none. If there are none - it returns permission denied.
#     """
#     def decorator(func):
#         @wraps(func)
#         def inner(request, kanban_card_id, *args, **kwargs):
#             # If user is admin - grant them all permissions
#             if request.user.is_superuser:
#                 # Return the function with a user_level of 4
#                 return func(request, kanban_card_id, *args, **kwargs, user_level=4)
#
#             passes, user_level = object_kanban_board(request, kanban_card_id)
#
#             if not passes:
#                 raise PermissionDenied
#
#             if user_level >= min_permission_level:
#                 # Everything is fine - continue on
#                 return func(
#                     request, kanban_card_id, *args, **kwargs, user_level=user_level
#                 )
#
#             # Does not meet conditions
#             raise PermissionDenied
#
#         return inner
#
#     return decorator
#
#
#
# def check_user_permissions(min_permission_level, object_lookup=""):
#     """
#     Check the user permissions - if they pass they can implement the function.
#     Otherwise send them to the permission denied page
#     """
#
#
#
# def check_user_requirement_item_permissions(min_permission_level):
#     """
#     Function is only used when checking user permissions against
#     customers - as they are different
#     """
#
#     def decorator(func):
#         @wraps(func)
#         def inner(request, *args, **kwargs):
#             # if user is admin -grant them all permissions
#             if request.user.is_superuser:
#                 # Return the function with a user_level of 4
#                 return func(request, *args, **kwargs, user_level=4)
#
#             passes, user_level = object_requirement_item(request, kwargs)
#
#             if not passes:
#                 raise PermissionDenied
#
#             if user_level >= min_permission_level:
#                 # Everything is fine - continue on
#                 return func(request, *args, **kwargs, user_level=user_level)
#
#             # Does not meet conditions
#             raise PermissionDenied
#
#         return inner
#
#     return decorator
#
#
# def check_rfc_permissions(min_permission_level):
#     """Check the user's RFC permissions"""
#
#     def decorator(func):
#         @wraps(func)
#         def inner(request, *args, **kwargs):
#             # If user is admin - grant them all permissions
#             if request.user.is_superuser:
#                 # Return the function with a user_level of 4
#                 return func(request, *args, **kwargs, user_level=4)
#
#             passes, user_level = object_rfc(request, kwargs)
#
#             if not passes:
#                 raise PermissionDenied
#
#             if user_level >= min_permission_level:
#                 # Everything is fine - continue on
#                 return func(request, *args, **kwargs, user_level=user_level)
#
#             # Does not meet conditions
#             raise PermissionDenied
#
#         return inner
#
#     return decorator
#
#
# #




