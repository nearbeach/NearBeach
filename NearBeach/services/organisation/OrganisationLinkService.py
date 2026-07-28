from typing import Tuple, Union, Dict
from rest_framework import status

from NearBeach.models import Organisation, Customer
from NearBeach.serializers.organisation_link_serializer import OrganisationLinkSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.utils.api.check_object_exists import check_object_exists
from NearBeach.utils.dicts.object_dict import OBJECT_DICT


class OrganisationLinkService(ObjectServiceAbstraction):
    """Class for create, read, update, delete of organisation links"""

    def create(self, request) -> Tuple[Union[Dict, str], int]:
        if not check_object_exists(self.destination, self.location_id):
            return "Object does not exist", status.HTTP_400_BAD_REQUEST

        serializer = OrganisationLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Get the object we wish to update
        # TODO - check to see if the OBJECT_DICT can be used from ABSTRACTED class
        update_object = OBJECT_DICT[self.destination].filter(
            is_deleted=False,
            pk=self.location_id,
        )

        # Check there is an object to update
        if len(update_object) == 0:
            return "No object exists", status.HTTP_400_BAD_REQUEST

        # Get organisation
        organisation_result = Organisation.objects.get(
            pk=serializer.validated_data["id"],
        )
        update_object.update(
            organisation=organisation_result,
        )

        # Send back data
        potential_customers = Customer.objects.filter(
            is_deleted=False,
            organisation_id=organisation_result.id,
        )

        # Serializer
        serializer = OrganisationLinkSerializer({
            "organisation": organisation_result,
            "potential_customers": potential_customers,
        })

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, object_id) -> Tuple[Union[Dict, str], int]:
        update_object = OBJECT_DICT[self.destination].filter(
            is_deleted=False,
            pk=self.location_id,
        )

        #Check there is an object to update
        if len(update_object) == 0:
            return "No object exists", status.HTTP_400_BAD_REQUEST

        # Remove organisation from object
        update_object.update(
            organisation=None,
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        pass

    def update(self, request, object_id) -> Tuple[Union[Dict, str], int]:
        pass
