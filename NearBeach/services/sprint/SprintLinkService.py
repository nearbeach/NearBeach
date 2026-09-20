from typing import Dict, Tuple, Union
from rest_framework import status
from NearBeach.models import (
    Sprint,
)
from NearBeach.serializers.sprint_serializer import SprintSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class SprintLinkService(ObjectServiceAbstraction):
    """Service dealing with sprint links to their parent requirement/projects"""

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

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        sprint_list = Sprint.objects.filter(
            is_deleted=False,
            **{self.destination: self.location_id},
        ).order_by('start_date', 'end_date', 'title')

        serializer = SprintSerializer(sprint_list, many=True)

        return serializer.data, status.HTTP_200_OK

    def update(self, request, sprint_id: int):
        pass