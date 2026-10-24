from rest_framework import status
from django.utils import timezone
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.serializers.user_list_serializer import UserListSerializer


class UserService(ObjectServiceAbstraction):
    """Service to help add and remove users against an object"""
    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        # Serialize the data for references
        serializer = UserListSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Loop through all the groups and add to the current object
        for single_user in serializer.validated_data["user_list"]:
            # Already on the object - adding it again would only create a duplicate row
            if ObjectAssignment.objects.filter(
                is_deleted=False,
                assigned_user_id=single_user.pk,
                **{F"{self.destination}_id": self.location_id},
            ).exists():
                continue

            # Construct the object assignment
            submit_object_assignment = ObjectAssignment(
                assigned_user_id=single_user.pk,
                change_user=request.user,
                **{F"{self.destination}_id": self.location_id},
            )

            # Save the data
            submit_object_assignment.save()

        return {}, status.HTTP_201_CREATED


    def delete(self, request: AuthenticatedRequest, user_id: ObjectId) -> ServiceResponse:
        remove_object_assignment = ObjectAssignment.objects.filter(
            assigned_user_id=int(user_id),
            **{F"{self.destination}_id": self.location_id}
        )

        # If there is nothing to delete, notify the user
        if len(remove_object_assignment) == 0:
            return "User assignment does not exist", status.HTTP_400_BAD_REQUEST

        # Remove the group
        remove_object_assignment.update(
            change_user=request.user,
            date_modified=timezone.now(),
            is_deleted=True,
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def update(self, request: AuthenticatedRequest, object_id: ObjectId) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class
