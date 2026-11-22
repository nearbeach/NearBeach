from NearBeach.api_docs import apply_schema
from NearBeach.api_docs.api_v1.request_for_change_docs import REQUEST_FOR_CHANGE_SCHEMA
from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.services.request_for_change.RequestForChangeService import RequestForChangeService
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.serializers.audit_log_serializer import AuditLogSerializer
from NearBeach.serializers.request_for_change_serializer import RequestForChangeSerializer
from NearBeach.services.AuditService import AuditService
from NearBeach.services.PublicLinkService import PublicLinkService
from NearBeach.services.customer.CustomerLinkService import CustomerLinkService
from NearBeach.services.LinkListService import LinkListService
from NearBeach.services.NoteService import NoteService
from NearBeach.services.organisation.OrganisationLinkService import OrganisationLinkService
from NearBeach.services.document.DocumentMiddlemanService import DocumentMiddlemanService
from NearBeach.services.document.DocumentService import DocumentService
from NearBeach.services.GroupService import GroupService
from NearBeach.services.UserService import UserService
from NearBeach.services.sprint.SprintLinkService import SprintLinkService


@apply_schema(REQUEST_FOR_CHANGE_SCHEMA)
class RequestForChangeViewSet(viewsets.ModelViewSet):
    queryset = RequestForChange.objects.filter(is_deleted=False)
    serializer_class = RequestForChangeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs) -> Response:
        request_for_change_service = RequestForChangeService(destination="request_for_change", location_id=0)
        data, http_status = request_for_change_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="audit",
    )
    def audit(self, request, pk, *args, **kwargs) -> Response:
        results = AuditService.get_list("request_for_change", pk)

        page = self.paginate_queryset(results)
        if page is not None:
            return self.get_paginated_response(AuditLogSerializer(page, many=True).data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="customer",
        pagination_class=None,
    )
    def customer(self, request, pk, *args, **kwargs) -> Response:
        customer_service = CustomerLinkService(destination="request_for_change", location_id=pk)

        # Get customer links
        data, http_status = customer_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @customer.mapping.post
    def customer_create(self, request, pk, *args, **kwargs) -> Response:
        customer_service = CustomerLinkService(destination="request_for_change", location_id=pk)

        # Create Link
        data, http_status = customer_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"customer/(?P<customer_pk>\d+)",
    )
    def customer_delete(self, request, pk, customer_pk, *args, **kwargs) -> Response:
        customer_service = CustomerLinkService(destination="request_for_change", location_id=pk)

        # Create Link
        data, http_status = customer_service.delete(request, customer_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request, pk, *args, **kwargs) -> Response:
        request_for_change_service = RequestForChangeService(destination="request_for_change", location_id=pk)
        if request_for_change_service.delete(request, None):
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data={"Object does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="documents",
    )
    def documents(self, _, pk, *args, **kwargs) -> Response:
        document_service = DocumentService(destination="request_for_change", location_id=pk)
        data, http_status = document_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="document")
    @documents.mapping.post
    def documents_create(self, request, pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="request_for_change", location_id=pk)
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
        document_middleman_service = DocumentMiddlemanService(destination="request_for_change", location_id=pk)
        data, http_status = document_middleman_service.delete(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @documents_delete.mapping.patch
    def documents_update(self, request, pk, document_pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="request_for_change", location_id=pk)
        data, http_status = document_middleman_service.update(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="groups"
    )
    def groups_list(self, _, pk, *args, **kwargs) -> Response:
        group_service = GroupService(destination="request_for_change", location_id=pk)
        data, http_status = group_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @groups_list.mapping.post
    def groups_list_create(self, request, pk, *args, **kwargs) -> Response:
        # Create a new connection first
        group_service = GroupService(destination="request_for_change", location_id=pk)
        data, http_status = group_service.create(request)

        # Check results
        if http_status != status.HTTP_201_CREATED:
            return Response(
                data=data,
                status=http_status,
            )

        # Utilise the get list method and send back the complete list
        data, http_status = group_service.get_list(request)

        return Response(
            data=data,
            status=status.HTTP_201_CREATED if http_status == status.HTTP_200_OK else http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"groups/(?P<group_pk>\d+)",
    )
    def groups_list_delete(self, request, pk, group_pk, *args, **kwargs) -> Response:
        # Delete a group
        group_service = GroupService(destination="request_for_change", location_id=pk)
        data, http_status = group_service.delete(request, group_pk)

        # If you cannot delete - notify the user
        if http_status != status.HTTP_204_NO_CONTENT:
            return Response(
                data=data,
                status=http_status,
            )

        # Utilise the get list method and send back the complete list
        data, http_status = group_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(methods=["GET"], detail=True, url_path="link_list", pagination_class=None)
    def link_list(self, _, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="request_for_change", location_id=pk)
        data, http_status = link_list_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list.mapping.post
    def link_list_create(self, request, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="request_for_change", location_id=pk)
        data, http_status = link_list_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"link_list/(?P<link_pk>\d+)")
    def link_list_delete(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="request_for_change", location_id=pk)
        data, http_status = link_list_service.delete(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list_delete.mapping.patch
    def link_list_update(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="request_for_change", location_id=pk)
        data, http_status = link_list_service.update(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @destination_permission(min_permission_level=1)
    def list(self, request, *args, **kwargs) -> Response:
        """Method for getting a list of all request_for_changes through search"""
        request_for_change_service = RequestForChangeService(destination="request_for_change", location_id=0)
        request_for_change_results = request_for_change_service.get_list(request)

        page = self.paginate_queryset(request_for_change_results)
        if page is not None:
            serializer = RequestForChangeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="notes",
        pagination_class=None,
    )
    def notes(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="request_for_change", location_id=pk)
        data, http_status = note_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="request_for_change_note")
    @notes.mapping.post
    def notes_create(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="request_for_change", location_id=pk)
        data, http_status = note_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="request_for_change_note")
    @action(
        methods=["DELETE"],
        detail=True,
        url_path = r"notes/(?P<note_pk>\d+)",
    )
    def notes_delete(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="request_for_change", location_id=pk)
        data, http_status = note_service.delete(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="request_for_change_note")
    @notes_delete.mapping.patch
    def notes_update(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="request_for_change", location_id=pk)
        data, http_status = note_service.update(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="organisation",
    )
    def organisation(self, request, pk, *args, **kwargs) -> Response:
        organisation_link_service = OrganisationLinkService(
            destination="request_for_change",
            location_id=pk
        )
        data, http_status = organisation_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @organisation.mapping.post
    def organisation_create(self, request, pk, *args, **kwargs) -> Response:
        organisation_service = OrganisationLinkService(
            destination="request_for_change", location_id=pk
        )
        data, http_status = organisation_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @organisation.mapping.delete
    def organisation_delete(self, request, pk, *args, **kwargs) -> Response:
        organisation_service = OrganisationLinkService(
            destination="request_for_change", location_id=pk
        )
        data, http_status = organisation_service.delete(request, pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, pk, *args, **kwargs) -> Response:
        request_for_change_services = RequestForChangeService(destination="request_for_change", location_id=pk)
        data, http_status = request_for_change_services.update(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="public_link",
        pagination_class=None,
    )
    def public_link(self, request, pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="request_for_change", location_id=pk)
        data, http_status = public_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link.mapping.post
    def public_link_create(self, request, pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="request_for_change", location_id=pk)
        data, http_status = public_link_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"public_link/(?P<public_link_pk>[0-9a-fA-F-]{36})"
    )
    def public_link_delete(self, request, pk, public_link_pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="request_for_change", location_id=pk)
        data, http_status = public_link_service.delete(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link_delete.mapping.patch
    def public_link_update(self, request, pk, public_link_pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="request_for_change", location_id=pk)
        data, http_status = public_link_service.update(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, pk, *args, **kwargs) -> Response:
        request_for_change_service = RequestForChangeService(destination="request_for_change", location_id=pk)
        data, http_status = request_for_change_service.retrieve(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="sprint",
        pagination_class=None,
    )
    def sprint(self, request, pk, *args, **kwargs):
        sprint_link_service = SprintLinkService(
            destination="request_for_change",
            location_id=pk,
        )
        data, http_status = sprint_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @sprint.mapping.post
    def sprint_create(self, request, pk, *args, **kwargs):
        sprint_link_service = SprintLinkService(destination="request_for_change", location_id=pk)
        data, http_status = sprint_link_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"sprint/(?P<sprint_pk>\d+)"
    )
    def sprint_delete(self, request, pk, sprint_pk, *args, **kwargs):
        sprint_link_service = SprintLinkService(destination="request_for_change", location_id=pk)
        data, http_status = sprint_link_service.delete(request, sprint_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["POST"], detail=True, url_path="users")
    def users_list_create(self, request, pk, *args, **kwargs) -> Response:
        # Create a new connection first
        user_service = UserService(destination="request_for_change", location_id=pk)
        data, http_status = user_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"users/(?P<user_pk>\d+)")
    def users_list_delete(self, request, pk, user_pk, *args, **kwargs) -> Response:
        # Delete user
        user_service = UserService(destination="request_for_change", location_id=pk)
        data, http_status = user_service.delete(request, user_pk)

        return Response(
            data=data,
            status=http_status,
        )
