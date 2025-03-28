from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.models import (
    Group,
    ObjectAssignment,
    User,
    UserGroup,
)
from NearBeach.serializers.destination_serializer import DestinationSerializer
from NearBeach.serializers.object_data.group_and_user_serializer import GroupAndUserSerializer
from NearBeach.views.object_data_views import get_group_and_user_list
from NearBeach.views.tools.internal_functions import set_object_from_destination


class GroupAndUserViewSet(viewsets.ViewSet):
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
        destination = serializer.data["destination"]
        location_id = serializer.data["location_id"]
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
        destination = serializer.data["destination"]
        location_id = serializer.data["location_id"]
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

    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Serialise the data
        serializer = DestinationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack the variables
        destination = serializer.data["destination"]
        location_id = serializer.data["location_id"]

        return Response(
            get_group_and_user_list(
                destination,
                location_id,
                request,
            )
        )
