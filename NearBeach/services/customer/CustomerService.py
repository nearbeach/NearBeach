from rest_framework import status
from rest_framework.serializers import Serializer

from NearBeach.models.customer import Customer
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)


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

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = CustomerSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        customer_submit = serializer.save(
            change_user=request.user,
        )

        serializer = CustomerSerializer(customer_submit)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, customer_pk: ObjectId) -> ServiceResponse:
        # TODO - this will change
        customer = Customer.objects.filter(pk=customer_pk, is_deleted=False).first()
        if customer is None:
            return "Customer does not exist", status.HTTP_400_BAD_REQUEST

        customer.is_deleted = True
        customer.change_user = request.user
        customer.save()

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = self._get_list()

        # Return list
        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, pk: ObjectId) -> ServiceResponse:
        customer = Customer.objects.filter(pk=pk, is_deleted=False).first()
        if customer is None:
            return "Customer does not exist", status.HTTP_400_BAD_REQUEST

        # TODO - check to see if we want to do partial updates
        serializer = CustomerSerializer(customer, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        updated_customer = serializer.save(change_user=request.user)

        return CustomerSerializer(updated_customer).data, status.HTTP_200_OK
