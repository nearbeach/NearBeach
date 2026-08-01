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
        pass

    def delete(self, request, sprint_id: int):
        pass

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        sprint_list = Sprint.objects.filter(
            is_deleted=False,
            **{self.destination: self.location_id},
        ).order_by('start_date', 'end_date', 'title')

        serializer = SprintSerializer(sprint_list, many=True)

        return serializer.data, status.HTTP_200_OK

    def update(self, request, sprint_id: int):
        pass