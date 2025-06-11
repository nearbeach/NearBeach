from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.customer_permissions import check_user_customer_permissions
from NearBeach.models import (
    Customer,
    ListOfTitle,
    Organisation,
)
from NearBeach.serializers.customer_serializer import CustomerSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

import datetime


class CustomerViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @check_user_customer_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Gather instances
        organisation_instance = Organisation.objects.get(
            organisation_id=serializer.data.get("organisation"),
        )

        customer_title_instance = ListOfTitle.objects.get(
            title_id=serializer.data.get("customer_title"),
        )

        # Create Customer
        customer_submit = Customer(
            customer_title=customer_title_instance,
            customer_first_name=serializer.data.get("customer_first_name"),
            customer_last_name=serializer.data.get("customer_last_name"),
            customer_email=serializer.data.get("customer_email"),
            organisation=organisation_instance,
            change_user=request.user,
        )
        customer_submit.save()

        return Response(
            data={"customer_id": customer_submit.customer_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_customer_permissions(min_permission_level=4)
    def destroy(self, request, pk=None, *args, **kwargs):
        customer = Customer.objects.get(pk=pk)
        customer.is_deleted = True
        customer.change_user = request.user
        customer.save()
        return Response(
            data='customer deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all customers within an organisation.

    """
    )
    @check_user_customer_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        customer_results = Customer.objects.filter(
            is_deleted=False,
            organisation_id=kwargs["organisation_id"],
        )

        serializer = CustomerSerializer(
            customer_results,
            many=True
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single customer within an organisation
        """
    )
    @check_user_customer_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        # Customer Results
        customer_results = get_object_or_404(
            queryset=Customer.objects.filter(
                is_deleted=False,
                organisation_id=kwargs["organisation_id"],
            ),
            pk=pk
        )

        serializer = CustomerSerializer(customer_results)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single customer under an organisation.

# 🧾 Parameters

- Customer First Name
- Customer Last Name
- Customer Email
- Customer Title: You can get a full list of title Id's from the database
    """
    )
    @check_user_customer_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get customer to update
        update_customer = get_object_or_404(
            queryset=Customer.objects.filter(
                is_deleted=False,
                organisation_id=kwargs["organisation_id"],
            ),
            pk=pk
        )
        update_customer.change_user = request.user
        update_customer = serializer.update(
            update_customer,
            serializer.data,
        )

        # Re-serialize data
        serializer = CustomerSerializer(update_customer, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
