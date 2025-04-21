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
# 📌 Description

This endpoint allows you to add either a user or a group to a specific object (e.g., Project, Task, Kanban Card, etc.).

To obtain valid user and group IDs, use the GET method on this endpoint and refer to the 'potential_user_list' and 
'potential_group_list' fields in the response.


# 🧾 Parameters

- Destination: The type of object you're linking to. Must be one of the following:
    - Kanban Card
    - Project
    - Request for Change
    - Requirement
    - Requirement Item
    - Task
- Location ID: The unique ID of the specific object you're modifying (e.g., the project ID or task ID).
- ID: This should always be set to 0. (This is a required field for request formatting, but not used during creation.)

# ✅ Notes
- Make sure the user or group you are trying to add appears in the potential_user_list or potential_group_list 
respectively. If not, they may already be associated with the object.
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

        # TODO - 0.32 - move this to a Serializer. This will help with documentation AND is best practise :)
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
# 📌 Description

This API endpoint provides group and user-related information for a specified object. It returns several categorized lists that can be used by the frontend to manage group and user assignments.

# Returned Fields:

- **Object Group List**: A list of groups currently assigned to the object.
- **Object User List**: A list of users currently assigned to the object.
- **Potential Group List**: A list of groups that *can* be assigned to the object.
- **Potential User List**: A list of users that *can* be assigned to the object.
- **User Group List**: A list of groups that the current authenticated user is a member of.

This endpoint is primarily used by the frontend in the "Group and User" section to retrieve relevant assignment data.

---

# 🧾 Parameters

- **Destination**: The type of object you are querying. Must be one of:
  - Kanban Card  
  - Project  
  - Request for Change  
  - Requirement  
  - Requirement Item  
  - Task  

- **Location ID**: The unique ID of the specific object instance.
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
