from NearBeach.api_docs import apply_schema
from NearBeach.api_docs.api_v1.organisation_docs import ORGANISATION_SCHEMA
from NearBeach.services.NoteService import NoteService
from NearBeach.services.document.DocumentMiddlemanService import DocumentMiddlemanService
from NearBeach.services.document.DocumentService import DocumentService
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Organisation
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.services.abstraction.object_services_abstraction import AuthenticatedRequest
from NearBeach.services.organisation.OrganisationService import OrganisationService
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.customer.CustomerService import CustomerService


@apply_schema(ORGANISATION_SCHEMA)
class OrganisationViewSet(viewsets.ModelViewSet):
    """Class for the organisation view set"""
    queryset = Organisation.objects.filter(is_deleted=False)
    serializer_class = OrganisationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request: AuthenticatedRequest, *args, **kwargs):
        """Create a new organisation"""
        organisation_services = OrganisationService(destination="organisation", location_id=0)
        data, http_status = organisation_services.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="customer",
    )
    def customer(self, request, pk, *args, **kwargs) -> Response:
        customer_services = CustomerService(destination="organisation", location_id=pk)
        customer_results = customer_services.get_list(request)

        page = self.paginate_queryset(customer_results)
        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @object_permission(min_permission_level=3)
    @customer.mapping.post
    def customer_create(self, request, pk, *args, **kwargs) -> Response:
        """Create a new customer for an organisation"""
        customer_services = CustomerService(destination="organisation", location_id=pk)
        data, http_status = customer_services.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path=r"customer/(?P<customer_pk>\d+)",
    )
    def customer_retrieve(self, _, pk, customer_pk, *args, **kwargs):
        customer_services = CustomerService(destination="organisation", location_id=pk)
        data, http_status = customer_services.retrieve(customer_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @customer_retrieve.mapping.patch
    def customer_update(self, request, pk, customer_pk, *args, **kwargs):
        customer_service = CustomerService(destination="organisation", location_id=pk)
        data, http_status = customer_service.update(request, customer_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=4)
    @customer_retrieve.mapping.delete
    def customer_delete(self, request, pk, customer_pk, *args, **kwargs) -> Response:
        """Delete a customer from an organisation"""
        customer_services = CustomerService(destination="organisation", location_id=pk)
        data, http_status = customer_services.delete(request, customer_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
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
    @action(
        methods=["GET"],
        detail=True,
        url_path="documents",
    )
    def documents(self, _, pk, *args, **kwargs) -> Response:
        document_service = DocumentService(destination="organisation", location_id=pk)
        data, http_status = document_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="document")
    @documents.mapping.post
    def documents_create(self, request, pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="organisation", location_id=pk)
        data, http_status = document_middleman_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"documents/(?P<document_pk>[^/.]+)",
    )
    def documents_delete(self, request, pk, document_pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="organisation", location_id=pk)
        data, http_status = document_middleman_service.delete(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @documents_delete.mapping.patch
    def documents_update(self, request, pk, document_pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="organisation", location_id=pk)
        data, http_status = document_middleman_service.update(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @destination_permission(min_permission_level=1)
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


    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="notes",
        pagination_class=None,
    )
    def notes(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="organisation", location_id=pk)
        data, http_status = note_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="organisation_note")
    @notes.mapping.post
    def notes_create(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="organisation", location_id=pk)
        data, http_status = note_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="organisation_note")
    @action(
        methods=["DELETE"],
        detail=True,
        url_path = r"notes/(?P<note_pk>\d+)",
    )
    def notes_delete(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="organisation", location_id=pk)
        data, http_status = note_service.delete(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="organisation_note")
    @notes_delete.mapping.patch
    def notes_update(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="organisation", location_id=pk)
        data, http_status = note_service.update(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )
