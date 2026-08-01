from typing import Tuple, Union, Dict
from rest_framework import status
from rest_framework.serializers import Serializer

from NearBeach.models import ObjectAssignment, Customer
from NearBeach.serializers.customer_link_serializer import CustomerLinkSerializer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class CustomerLinkService(ObjectServiceAbstraction):
    """Class for create, read, update, delete of customer links"""

    def _get_list(self) -> Serializer:
        # Send back data to user
        customer_results = Customer.objects.filter(
            id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                customer_id__isnull=False,
                **{F"{self.destination}_id": self.location_id},
            ).values("customer_id"),
        )

        serializer = CustomerSerializer(customer_results, many=True)

        return serializer

    def create(self, request) -> Tuple[Union[Dict, str], int]:
        serializer = CustomerLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Add customer to object
        submit_object_assignment = ObjectAssignment(
            customer_id=serializer.validated_data['id'],
            change_user=request.user,
            **{F"{self.destination}_id": self.location_id},
        )

        # Save the data
        submit_object_assignment.save()

        # Send back data to user
        serializer = self._get_list()

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, object_id) -> Tuple[Union[Dict, str], int]:
        # Get the object link
        object_assignment_results = ObjectAssignment.objects.filter(
            customer_id=object_id,
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )

        if len(object_assignment_results) == 0:
            return "Can not find customer/object connection", status.HTTP_400_BAD_REQUEST

        # Update the results
        object_assignment_results.update(
            is_deleted=True,
        )

        # Send data back to user
        serializer = self._get_list()

        return serializer.data, status.HTTP_200_OK

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        pass

    def update(self, request, object_id) -> Tuple[Union[Dict, str], int]:
        pass
