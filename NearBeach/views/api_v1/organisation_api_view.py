from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Organisation
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.services.abstraction.object_services_abstraction import AuthenticatedRequest
from NearBeach.services.organisation.OrganisationService import OrganisationService


class OrganisationViewSet(viewsets.ModelViewSet):
    """Class for the organisation view set"""
    queryset = Organisation.objects.filter(is_deleted=False)
    serializer_class = OrganisationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    @object_permission(min_permission_level=3)
    def create(request: AuthenticatedRequest, *args, **kwargs):
        """Create a new organisation"""
        organisation_services = OrganisationService(destination="organisation", location_id=0)
        data, http_status = organisation_services.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def destroy(request, pk, *args, **kwargs) -> Response:
        """Delete an organisation"""
        organisation_services = OrganisationService(
            destination="organisation",
            location_id=pk
        )
        data, http_status = organisation_services.delete(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    def list(self, request: AuthenticatedRequest, *args, **kwargs):
        organisation_services = OrganisationService(destination="organisation", location_id=0)
        organisation_results = organisation_services.get_list(request)

        page = self.paginate_queryset(organisation_results)
        if page is not None:
            serializer = OrganisationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, pk, *args, **kwargs) -> Response:
        organisation_service = OrganisationService(destination="organisation", location_id=pk)
        data, http_status = organisation_service.update(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, pk, *args, **kwargs):
        organisation_service = OrganisationService(destination="organisation", location_id=pk)
        data, http_status = organisation_service.retrieve()

        return Response(
            data=data,
            status=http_status,
        )
