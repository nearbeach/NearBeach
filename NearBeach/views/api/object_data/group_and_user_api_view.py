from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.models import (
    Group,
    ObjectAssignment,
    User,
    UserGroup,
)
from NearBeach.serializers.object_data.group_and_user_serializer import GroupAndUserSerializer
from NearBeach.views.object_data_views import get_group_and_user_list
from NearBeach.views.tools.internal_functions import set_object_from_destination

@extend_schema(
    tags=["Object Data|Groups And Users"]
)
class GroupAndUserViewSet(viewsets.ViewSet):
    serializer_class = GroupAndUserSerializer

    @extend_schema(
        description="""
Add either a user(s) or a group(s) to this object. The IDs for the users and groups can be obtained by
using the GET functionality, and looking at the "potential_group_list" or "potential_user_list" fields within 
the response.

Parameters

Destination is the object you are looking up. It can only be;
- Kanban Card
- Project
- Request for Change
- Requirement
- Requirement Item
- Task

The Location Id, is the ID number of that specific object.

The ID is a integer field, just leave as 0
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Add both user 2, and 3 to the current object",
                value={"user_list": [2, 3]},
            ),
            OpenApiExample(
                "Example 2",
                description="Add the group 5 to the current project",
                value={"group_list": 5},
            ),
        ],
    )
    @api_object_data_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        # Serialize the data for references
        serializer = GroupAndUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack the variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        group_list = serializer.data["group_list"]
        user_list = serializer.data["user_list"]

        # Loop through all the groups and add to the current object
        for single_group in group_list:
            # Get group instance
            group_instance = Group.objects.get(group_id=single_group)

            # Construct the object assignment
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                change_user=request.user,
            )
            submit_object_assignment = set_object_from_destination(
                submit_object_assignment, destination, location_id
            )

            # Save the data
            submit_object_assignment.save()

        # Get the current permission/groups for this object
        object_groups = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
            **{F"{destination}_id": location_id},
        ).values('group_id')
        error_array = []

        for single_user in user_list:
            # Get user instance
            user_instance = User.objects.get(id=single_user)

            # Check to make sure the user has any of the groups assigned to the object
            user_group_count = len(
                UserGroup.objects.filter(
                    is_deleted=False,
                    username_id=single_user,
                    group_id__in=object_groups,
                )
            )
            if user_group_count == 0:
                # We can not add current user to the object. Notify the user
                error_array.append({
                    "user": user_instance.id,
                    "username": user_instance.username,
                })
                continue

            # Create object assignment
            submit_object_assignment = ObjectAssignment(
                change_user=request.user,
                assigned_user=user_instance,
            )
            submit_object_assignment = set_object_from_destination(
                submit_object_assignment, destination, location_id
            )

            # Save
            submit_object_assignment.save()

        return_data = get_group_and_user_list(
            destination,
            location_id,
            request,
        )
        status_code = status.HTTP_201_CREATED

        if len(error_array) > 0:
            return_data["error_array"] = error_array
            return_data["error_message"] = "Users in Error Array can not be added to object, as their groups are not assigned to object"
            status_code = status.HTTP_403_FORBIDDEN

        return Response(
            return_data,
            status_code,
        )

    @extend_schema(
        description="""
Remove either a single user or a single group from this object. The IDs for the users and groups can be obtained by
using the GET functionality.

Parameters

Destination is the object you are looking up. It can only be;
- Kanban Card
- Project
- Request for Change
- Requirement
- Requirement Item
- Task

The Location Id, is the ID number of that specific object.

The ID is a integer field, just leave as 0
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Remove user (2) from the current project",
                value={"user": 2},
            ),
            OpenApiExample(
                "Example 2",
                description="Remove group (3) from the current project",
                value={"user": 3},
            ),
        ],
    )
    @api_object_data_permissions(min_permission_level=2)
    def destroy(self, request, pk=None, *args, **kwargs):
        # Serialise the data
        serializer = GroupAndUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack the variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        group = serializer.data.get("group", None)
        user = serializer.data.get("user", None)

        if group is not None:
            # First check that there are enough groups to delete.
            check_object_groups = len(
                ObjectAssignment.objects.filter(
                    is_deleted=False,
                    group_id__isnull=False,
                    **{F"{destination}_id": location_id},
                ).exclude(
                    group_id=group,
                )
            )

            # If there is no data - we can't delete this last group
            if check_object_groups == 0:
                return Response(
                    data={ "Error": "Can not remove last group" },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Delete the group
            ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id=group,
            ).update(
                is_deleted=True,
            )

        if user is not None:
            # Delete the users
            ObjectAssignment.objects.filter(
                is_deleted=False,
                assigned_user_id=user,
                **{F"{destination}_id": location_id }
            ).update(
                is_deleted=True,
            )

        return Response(
            get_group_and_user_list(
                destination,
                location_id,
                request,
            )
        )

    @extend_schema(
        description="""
Group and User API end point supplies the following information on a given object;
- Object Group List -> A list of groups assigned to current object
- Object User List -> A list of users assigned to current object
- Potential Group List -> Potential groups that can be assigned to object
- Potential User List -> Potential users that can be assigned to object
- User Group List -> Current user's list of groups they have been assigned to.

This list is used by the front end for the Group and User section. It can be used to obtain any of the data
outlined above.

Parameters

Destination is the object you are looking up. It can only be;
- Kanban Card
- Project
- Request for Change
- Requirement
- Requirement Item
- Task

The Location Id, is the ID number of that specific object.
            """,
    )
    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Flat pack the variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # TODO - Add in destination check - not all destination objects can be utilised for this function :)

        return Response(
            get_group_and_user_list(
                destination,
                location_id,
                request,
            )
        )
