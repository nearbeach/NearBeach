from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.api_docs import apply_schema
from NearBeach.api_docs.api_v1.customer_docs import CUSTOMER_SCHEMA
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Customer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import AuthenticatedRequest
from NearBeach.services.customer.CustomerService import CustomerService


@apply_schema(CUSTOMER_SCHEMA)
class CustomerViewSet(viewsets.ModelViewSet):
    """Class for the customer view set"""
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    @object_permission(min_permission_level=3)
    def create(request: AuthenticatedRequest, organisation_id, *args, **kwargs) -> Response:
        """Create a new customer for an organisation"""
        customer_services = CustomerService(destination="organisation", location_id=organisation_id)
        data, http_status = customer_services.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def delete(request: AuthenticatedRequest, organisation_id, pk, *args, **kwargs) -> Response:
        """Delete a customer from an organisation"""
        customer_services = CustomerService(destination="organisation", location_id=organisation_id)
        data, http_status = customer_services.delete(request, pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    def list(self, request: AuthenticatedRequest, organisation_id, *args, **kwargs) -> Response:
        customer_services = CustomerService(destination="organisation", location_id=organisation_id)
        customer_results = customer_services.get_list(request)

        page = self.paginate_queryset(customer_results)
        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(_, organisation_id, pk, *args, **kwargs):
        customer_services = CustomerService(destination="organisation", location_id=organisation_id)
        data, http_status = customer_services.retrieve(pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def update(request: AuthenticatedRequest, organisation_id, pk, *args, **kwargs):
        customer_service = CustomerService(destination="organisation", location_id=organisation_id)
        data, http_status = customer_service.update(request, pk)

        return Response(
            data=data,
            status=http_status,
        )
