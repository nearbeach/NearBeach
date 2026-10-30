from django.db.models import QuerySet, Q
from rest_framework import status

from NearBeach.models.customer import Customer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class CustomerService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete customer objects"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = CustomerSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        customer_submit = serializer.save(
            change_user=request.user,
            organisation_id=self.location_id,
        )

        serializer = CustomerSerializer(customer_submit)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, customer_pk: int) -> ServiceResponse:
        """Method to delete a customer"""
        customer = Customer.objects.filter(
            pk=customer_pk,
            organisation_id=self.location_id,
            is_deleted=False,
        )
        if not customer.exists():
            return "Customer does not exist", status.HTTP_400_BAD_REQUEST

        customer.update(
            is_deleted=True,
            change_user=request.user,
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request: AuthenticatedRequest) -> QuerySet[Customer]:  # type: ignore[override]
        customer_results = Customer.objects.filter(
            is_deleted=False,
        ).order_by("last_name", "first_name", "pk")

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search:
            customer_results = customer_results.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(id=int(search) if search.isdigit() else None)
            )

        return customer_results

    def retrieve(self, customer_pk: ObjectId) -> ServiceResponse:
        organisation = Customer.objects.filter(
            is_deleted=False,
            pk=customer_pk,
            organisation_id=self.location_id,
        )

        if not organisation.exists():
            return "Customer does not exist", status.HTTP_404_NOT_FOUND

        # Serialize the data
        serializer = CustomerSerializer(
            organisation.first(),
            many=False
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, customer_pk: int) -> ServiceResponse:
        customer = Customer.objects.filter(
            pk=customer_pk,
            is_deleted=False,
            organisation_id=self.location_id,
        )
        if not customer.exists():
            return "Customer does not exist", status.HTTP_400_BAD_REQUEST

        # Prepare serializer for update
        serializer = CustomerSerializer(customer, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Apply updates
        updated_customer = serializer.save(change_user=request.user)

        # Return results
        return updated_customer.data, status.HTTP_200_OK
