from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.services.ProjectService import ProjectService
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Project
from NearBeach.serializers.project_serializer import ProjectSerializer
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


@extend_schema(
    tags=["Projects"],
    methods=["GET", "POST", "PATCH", "DELETE"],
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs) -> Response:
        project_service = ProjectService(destination="project", location_id=0)
        data, http_status = project_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["POST"],
        detail=True,
        url_path="customer",
    )
    def customer(self, request, pk, *args, **kwargs) -> Response:
        customer_service = CustomerLinkService(destination="project", location_id=pk)

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
        url_path=r"customer/(?P<customer_pk>[^/.]+)",
    )
    def customer_delete(self, _, pk, customer_pk, *args, **kwargs) -> Response:
        customer_service = CustomerLinkService(destination="project", location_id=pk)

        # Create Link
        data, http_status = customer_service.delete(customer_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request, pk, *args, **kwargs) -> Response:
        project_service = ProjectService(destination="project", location_id=pk)
        if project_service.delete(request, None):
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
        document_service = DocumentService(destination="project", location_id=pk)
        data, http_status = document_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @documents.mapping.post
    def documents_create(self, request, pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="project", location_id=pk)
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
        document_middleman_service = DocumentMiddlemanService(destination="project", location_id=pk)
        data, http_status = document_middleman_service.delete(request, document_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @documents.mapping.patch
    def documents_update(self, request, pk, document_pk, *args, **kwargs) -> Response:
        document_middleman_service = DocumentMiddlemanService(destination="project", location_id=pk)
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
        group_service = GroupService(destination="project", location_id=pk)
        data, http_status = group_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @groups_list.mapping.post
    def groups_list_create(self, request, pk, *args, **kwargs) -> Response:
        # Create a new connection first
        group_service = GroupService(destination="project", location_id=pk)
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
        url_path=r"groups/(?P<group_pk>[^/.]+)",
    )
    def groups_list_delete(self, request, pk, group_pk, *args, **kwargs) -> Response:
        # Delete a group
        group_service = GroupService(destination="project", location_id=pk)
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
    @action(methods=["GET"], detail=True, url_path="link_list")
    def link_list(self, _, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="project", location_id=pk)
        data, http_status = link_list_service.get_list(_)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list.mapping.post
    def link_list_create(self, request, pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="project", location_id=pk)
        data, http_status = link_list_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"link_list/(?P<link_pk>[^/.]+)")
    def link_list_delete(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="project", location_id=pk)
        data, http_status = link_list_service.delete(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @link_list_delete.mapping.patch
    def link_list_update(self, request, pk, link_pk, *args, **kwargs) -> Response:
        link_list_service = LinkListService(destination="project", location_id=pk)
        data, http_status = link_list_service.update(request, link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @destination_permission(min_permission_level=1)
    def list(self, request, *args, **kwargs) -> Response:
        """Method for getting a list of all projects through search"""
        project_service = ProjectService(destination="project", location_id=0)
        project_results = project_service.get_list(request)

        page = self.paginate_queryset(project_results)
        if page is not None:
            serializer = ProjectSerializer(page, many=True)
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
    )
    def notes(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="project", location_id=pk)
        data, http_status = note_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @notes.mapping.post
    def notes_create(self, request, pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="project", location_id=pk)
        data, http_status = note_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"notes/(?P<note_pk>[^/.]+)")
    def notes_delete(self, request, pk, note_pk, *args, **kwargs) -> Response:
        note_service = NoteService(destination="project", location_id=pk)
        data, http_status = note_service.delete(request, note_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @notes_delete.mapping.post
    def notes_update(self, request, pk, note_pk) -> Response:
        note_service = NoteService(destination="project", location_id=pk)
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
            destination="project",
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
            destination="project", location_id=pk
        )
        data, http_status = organisation_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @organisation.mapping.delete
    def organisation_delete(self, _, pk, *args, **kwargs) -> Response:
        organisation_service = OrganisationLinkService(
            destination="project", location_id=pk
        )
        data, http_status = organisation_service.delete()

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, pk, *args, **kwargs) -> Response:
        project_services = ProjectService(destination="project", location_id=pk)
        data, http_status = project_services.update(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="public_link",
    )
    def public_link(self, request, pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="project", location_id=pk)
        data, http_status = public_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link.mapping.post
    def public_link_create(self, request, pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="project", location_id=pk)
        data, http_status = public_link_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(
        methods=["DELETE"],
        detail=True,
        url_path=r"public_link/(?P<public_link_pk>[^/.]+)"
    )
    def public_link_delete(self, request, pk, public_link_pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="project", location_id=pk)
        data, http_status = public_link_service.delete(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @public_link_delete.mapping.patch
    def public_link_update(self, request, pk, public_link_pk, *args, **kwargs):
        public_link_service = PublicLinkService(destination="project", location_id=pk)
        data, http_status = public_link_service.update(request, public_link_pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, pk, *args, **kwargs) -> Response:
        project_service = ProjectService(destination="project", location_id=pk)
        data, http_status = project_service.retrieve(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=1)
    @action(
        methods=["GET"],
        detail=True,
        url_path="sprint"
    )
    def sprint(self, request, pk, *args, **kwargs):
        sprint_link_service = SprintLinkService(
            destination="project",
            location_id=pk,
        )
        data, http_status = sprint_link_service.get_list(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["POST"], detail=True, url_path="users")
    def users_list_create(self, request, pk, *args, **kwargs) -> Response:
        # Create a new connection first
        user_service = UserService(destination="project", location_id=pk)
        data, http_status = user_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @object_permission(min_permission_level=2)
    @action(methods=["DELETE"], detail=True, url_path=r"users/(?P<user_pk>[^/.]+)")
    def users_list_delete(self, request, pk, user_pk, *args, **kwargs) -> Response:
        # Delete user
        user_service = UserService(destination="project", location_id=pk)
        data, http_status = user_service.delete(request, user_pk)

        return Response(
            data=data,
            status=http_status,
        )
