from NearBeach.models import (
    Sprint,
)
from NearBeach.serializers.sprint_serializer import SprintSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.utils.api.check_object_exists import check_object_exists
from NearBeach.utils.objects.error_object import ErrorObject


class SprintLinkService(ObjectServiceAbstraction):
    """Service dealing with sprint links to their parent requirement/projects"""

    def create(self, request):
        # TODO - Find out when we create a sprint, do we automatically link it to a specific requirement/project
        # If so - this step might not be needed :)
        pass

    def delete(self, request, sprint_id: int):
        """Method to delete a sprint link"""
        # TODO - Find out where this CRUD section should be - most likely on the sprint specific service
        # sprint_results = Sprint.objects.filter(
        #     is_deleted=False,
        #     pk=sprint_id,
        #     **{self.destination: self.location_id},
        # )
        #
        # if len(sprint_results) == 0:
        #     return False
        #
        # sprint_results.update(
        #     is_deleted=True,
        # )
        #
        # return True
        pass

    def get_list(self, request):
        """Method to get a list of sprints associated with current object"""
        if not check_object_exists(self.destination, self.location_id):
            return ErrorObject("Object does not exist"), False

        sprint_list = Sprint.objects.filter(
            is_deleted=False,
            **{self.destination: self.location_id},
        ).order_by('start_date', 'end_date', 'title')

        return SprintSerializer(sprint_list, many=True), True

    def update(self, request, sprint_id: int):
        pass