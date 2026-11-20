from NearBeach.api_docs import apply_schema
from NearBeach.api_docs.api_v1.requirement_item_docs import REQUIREMENT_ITEM_SCHEMA
from NearBeach.services.RequirementItemService import RequirementItemService
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.serializers.audit_log_serializer import AuditLogSerializer
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.services.AuditService import AuditService
from NearBeach.services.PublicLinkService import PublicLinkService
from NearBeach.services.LinkListService import LinkListService
from NearBeach.services.NoteService import NoteService
from NearBeach.services.document.DocumentMiddlemanService import DocumentMiddlemanService
from NearBeach.services.document.DocumentService import DocumentService
from NearBeach.services.sprint.SprintLinkService import SprintLinkService
from NearBeach.services.abstraction.object_services_abstraction import AuthenticatedRequest


@apply_schema(REQUIREMENT_ITEM_SCHEMA)
class RequirementItemViewSet(viewsets.ModelViewSet):
    queryset = RequirementItem.objects.filter(is_deleted=False)
    serializer_class = RequirementItemSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    @staticmethod
    @object_permission(min_permission_level=3)
    def create(request: AuthenticatedRequest, requirement_id, *args, **kwargs) -> Response:
        requirement_item_service = RequirementItemService(destination="requirement", location_id=requirement_id)
        data, http_status = requirement_item_service.create(request)

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
        results = AuditService.get_list("requirement_item", pk)

        page = self.paginate_queryset(results)
        if page is not None:
            return self.get_paginated_response(AuditLogSerializer(page, many=True).data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request: AuthenticatedRequest, requirement_id, pk, *args, **kwargs) -> Response:
        requirement_item_service = RequirementItemService(destination="requirement", location_id=requirement_id)
        data, http_status = requirement_item_service.delete(request, pk)

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
        document_service = DocumentService(destination="requirement_item", location_id=pk)
        data, http_status = document_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="document")
    @documents.mapping.post
    def documents_create(self, request, pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="requirement_item", location_id=pk)
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
        document_middleman_service = DocumentMiddlemanService(destination="requirement_item", location_id=pk)
        data, http_status = document_middleman_service.delete(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @documents_delete.mapping.patch
    def documents_update(self, request, pk, document_pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="requirement_item", location_id=pk)
        data, http_status = document_middleman_service.update(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(methods=["GET"], detail=True, url_path="link_list", pagination_class=None)
    def link_list(self, _, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="requirement_item", location_id=pk)
        data, http_status = link_list_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list.mapping.post
    def link_list_create(self, request, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="requirement_item", location_id=pk)
        data, http_status = link_list_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"link_list/(?P<link_pk>\d+)")
    def link_list_delete(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="requirement_item", location_id=pk)
        data, http_status = link_list_service.delete(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list_delete.mapping.patch
    def link_list_update(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="requirement_item", location_id=pk)
        data, http_status = link_list_service.update(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    def list(self, request: AuthenticatedRequest, requirement_id, *args, **kwargs) -> Response:
        """Method for getting a list of all requirement_items through search"""
        requirement_item_service = RequirementItemService(destination="requirement", location_id=requirement_id)
        requirement_item_results = requirement_item_service.get_list(request)

        page = self.paginate_queryset(requirement_item_results)
        if page is not None:
            serializer = RequirementItemSerializer(page, many=True)
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
        note_service = NoteService(destination="requirement_item", location_id=pk)
        data, http_status = note_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="requirement_item_note")
    @notes.mapping.post
    def notes_create(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="requirement_item", location_id=pk)
        data, http_status = note_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="requirement_item_note")
    @action(
        methods=["DELETE"],
        detail=True,
        url_path = r"notes/(?P<note_pk>\d+)",
    )
    def notes_delete(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="requirement_item", location_id=pk)
        data, http_status = note_service.delete(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2, additive_permission="requirement_item_note")
    @notes_delete.mapping.patch
    def notes_update(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="requirement_item", location_id=pk)
        data, http_status = note_service.update(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request: AuthenticatedRequest, requirement_id, pk, *args, **kwargs) -> Response:
        requirement_item_services = RequirementItemService(destination="requirement", location_id=requirement_id)
        data, http_status = requirement_item_services.update(request, pk)

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
        public_link_service = PublicLinkService(destination="requirement_item", location_id=pk)
        data, http_status = public_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link.mapping.post
    def public_link_create(self, request, pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="requirement_item", location_id=pk)
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
        public_link_service = PublicLinkService(destination="requirement_item", location_id=pk)
        data, http_status = public_link_service.delete(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link_delete.mapping.patch
    def public_link_update(self, request, pk, public_link_pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="requirement_item", location_id=pk)
        data, http_status = public_link_service.update(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request: AuthenticatedRequest, requirement_id, pk, *args, **kwargs) -> Response:
        requirement_item_service = RequirementItemService(destination="requirement", location_id=requirement_id)
        data, http_status = requirement_item_service.retrieve(request, pk)

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
        # TODO - Potential issue. If someone uses requirement that they have permission too, but then a requirement item they DON'T have access too - can they exploit out the sprints?
        sprint_link_service = SprintLinkService(
            destination="requirement_item",
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
        sprint_link_service = SprintLinkService(destination="requirement_item", location_id=pk)
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
        sprint_link_service = SprintLinkService(destination="requirement_item", location_id=pk)
        data, http_status = sprint_link_service.delete(request, sprint_pk)

        return Response(
            data=data,
            status=http_status,
        )
