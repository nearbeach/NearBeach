from typing import Dict, Tuple, Union
from rest_framework import status

from NearBeach.models import Sprint, ObjectAssignment
from NearBeach.serializers.sprint_serializer import SprintSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class SprintService(ObjectServiceAbstraction):
    """Service to help create, read, update, delete sprint objects"""
    # TODO - actually implement this functionality

    def create(self, request):
        """Method for creating a new sprint"""
        serializer = SprintSerializer(
            context={
                "request": request,
                "method": "POST",
            },
            data=request.data,
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Create the sprint
        created_sprint = serializer.save(
            change_user=request.user, creation_user=request.user
        )

        # Re-serialize the created project so it is in the same shape for the user
        serializer = SprintSerializer(created_sprint, many=False)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, sprint_id: int) -> Tuple[Union[Dict, str], int]:
        sprint_results = Sprint.objects.filter(
            is_deleted=False,
            pk=sprint_id,
            **{self.destination: self.location_id},
        )

        if len(sprint_results) == 0:
            return "Object does not exist", status.HTTP_400_BAD_REQUEST

        sprint_results.update(
            is_deleted=True,
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request):
        pass

    def retrieve(self, request) -> Tuple[Union[Dict, str], int]:
        # Get object
        sprint_results = Sprint.objects.get(pk=self.location_id)

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            project_id=self.location_id,
        )

        # Define groups list
        # sprint_results.group_list = Group.objects.filter(
        #     is_deleted=False,
        #     id__in=object_assignments.filter(
        #         group_id__isnull=False,
        #     ).values("group_id"),
        # )

        # Define user list
        # project_results.user_list = User.objects.filter(
        #     pk__in=object_assignments.filter(
        #         assigned_user__isnull=False,
        #     ).values("assigned_user_id"),
        # ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = SprintSerializer(
            sprint_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request, sprint_id: int):
        # Get project
        sprint = Sprint.objects.get(pk=self.location_id)

        # Setup serializer
        serializer = SprintSerializer(
            sprint,
            data=request.data,
            context={
                "request": request,
                "method": "PATCH",
            },
            partial=True,
        )
        if not serializer.is_valid():
            return serializer.errors, False

        # Make sure we update the change user
        serializer.change_user = request.user
        serializer.save()

        return serializer.data, status.HTTP_200_OK
