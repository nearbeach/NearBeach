from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.customer_permissions import check_user_customer_permissions
from NearBeach.serializers.destination_serializer import DestinationSerializer
from NearBeach.serializers.available_data.customer_list_serializer import CustomerListSerializer
from NearBeach.models import (
    Customer,
    Requirement,
    RequirementItem,
    Project,
    Task,
)

OBJECT_DICT = {
    "requirement": Requirement.objects,
    "requirement_item": RequirementItem.objects,
    "project": Project.objects,
    "task": Task.objects,
}


@extend_schema(
    tags=["Available Data"]
)
class CustomerListViewSet(viewsets.ViewSet):
    serializer_class = CustomerListSerializer

    @extend_schema(
        request=DestinationSerializer,
        responses={200: CustomerListSerializer},
    )
    @check_user_customer_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Serialise the data
        serializer = DestinationSerializer(data=request.query_params)
        # breakpoint()
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack the variables
        destination = serializer.data["destination"]
        location_id = serializer.data["location_id"]

        # Check the destination is of the limited sub object group
        if destination not in ["requirement", "requirement_item", "project", "task"]:
            return Response(
                data={"destination": "Current Destination does not have any customer associated with it"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get object and make sure it exists
        queryset = OBJECT_DICT[destination].filter(
            is_deleted=False,
        )
        object_results = get_object_or_404(
            queryset,
            pk=location_id,
        )

        # Get the organisation id
        if destination == "requirement_item":
            # Destroy the child object, insert the parent as it contains the organisation id
            object_results = object_results.requirement

        organisation_id = object_results.organisation_id

        # Get the customers connected to the organisation
        serializer = CustomerListSerializer(
            Customer.objects.filter(
                is_deleted=False,
                organisation_id=organisation_id,
            ),
            many=True,
        )

        return Response(serializer.data)
