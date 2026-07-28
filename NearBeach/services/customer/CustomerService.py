from typing import Dict, Tuple, Union
from rest_framework import status
from rest_framework.serializers import Serializer

from NearBeach.models import (
    Customer, ObjectAssignment
)
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class CustomerService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete customer objects"""

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
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        customer_submit = serializer.save(
            change_user=request.user,
        )

        serializer = CustomerSerializer(customer_submit)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, customer_pk: int) -> Tuple[Union[Dict, str], int]:
        # TODO - this will change
        customer = Customer.objects.get(pk=customer_pk)
        customer.is_deleted = True
        customer.change_user = request.user
        customer.save()

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        serializer = self._get_list()

        # Return list
        return serializer.data, status.HTTP_200_OK

    def update(self, request, pk) -> Tuple[Union[Dict, str], int]:
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # TODO - check how we want to use serializers to update objects
        # TODO - check to see if we want to do partial updates
        # Update serializer
        serializer.change_user = request.user
        serializer.save()

        return serializer.data, status.HTTP_200_OK
