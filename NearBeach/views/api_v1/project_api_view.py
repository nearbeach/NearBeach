from django.contrib.auth.models import User
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Project, ObjectAssignment, UserGroup, Group
from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.services.CustomerService import CustomerService
from NearBeach.services.LinkListService import LinkListService
from NearBeach.services.NoteService import NoteService
from NearBeach.services.OrganisationService import OrganisationService
from NearBeach.services.document.DocumentLinkService import DocumentLinkService
from NearBeach.services.document.DocumentService import DocumentService
from NearBeach.services.document.FolderService import FolderService
from NearBeach.utils.api.check_group_list import check_group_list
from NearBeach.services.GroupService import GroupService
from NearBeach.services.UserService import UserService


@extend_schema(
    tags=["Projects"],
    methods=["GET", "POST", "PATCH", "DELETE"],
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs):
        serializer = ProjectSerializer(
            context={
                'request': request,
                'method': 'POST',
            },
            data=request.data,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check that there exists groups
        group_list = request.data.getlist('group_list', [])
        if not check_group_list(request.user, group_list):
            return Response(
                "No Access to groups provided",
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create the project
        created_project = serializer.save(
            change_user=request.user,
            creation_user=request.user
        )

        # Re-serialize the created project so it is in the same shape for the user
        serializer = ProjectSerializer(created_project, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['POST'],
        detail=True,
        url_path='customer',
    )
    def customer(self, request, pk, *args, **kwargs):
        customer_service = CustomerService(destination="project", location_id=pk)

        # Create Link
        serializer, success = customer_service.link_customer(request)
        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path='customer',
    )
    def customer_delete(self, _, pk, *args, **kwargs):
        customer_service = CustomerService(destination="project", location_id=pk)

        # Create Link
        serializer, success = customer_service.unlink_customer(pk)
        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request, pk, *args, **kwargs):
        project = get_object_or_404(
            Project.objects.filter(is_deleted=False),
            pk=pk
        )
        project.is_deleted = True
        project.change_user = request.user
        project.save()
        return Response(
            data='project deleted',
            status=status.HTTP_204_NO_CONTENT,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['GET'],
        detail=True,
        url_path='documents',
    )
    def documents(self, _, pk, *args, **kwargs):
        document_service = DocumentService(destination="project", location_id=pk)
        serializer = document_service.get_list(_)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @documents.mapping.post
    def documents_create(self, request, pk, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Defined variables
        success = False

        # TODO - move this into the service
        # Depending on the type - depends on what we do
        match serializer.validated_data['type']:
            case "folder":
                folder_service = FolderService(destination="project", location_id=pk)
                return_serializer, success = folder_service.create(request)
            case "link":
                link_service = DocumentLinkService(destination="project", location_id=pk)
                return_serializer, success = link_service.create(request)
            case _:
                document_service = DocumentService(destination="project", location_id=pk)
                return_serializer, success = document_service.create(request)

        if success:
            return Response(
                data=return_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'documents/(?P<document_pk>[^/.]+)'
    )
    def documents_delete(self, request, pk, document_pk, *args, **kwargs):
        serializer = DocumentDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # TODO - Remove this switch statement into the service
        # Depending on the type - depends on what we do
        match serializer.validated_data['type']:
            case "folder":
                folder_service = FolderService(destination="project", location_id=pk)
                if folder_service.delete(request, document_pk):
                    return Response(status=status.HTTP_204_NO_CONTENT)
            case "link":
                link_service = DocumentLinkService(destination="project", location_id=pk)
                if link_service.delete(request, document_pk):
                    return Response(status=status.HTTP_204_NO_CONTENT)
            case _:
                document_service = DocumentService(destination="project", location_id=pk)
                if document_service.delete(request, document_pk):
                    return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @documents.mapping.patch
    def documents_update(self, request, pk, document_pk, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Depending on the type - depends on what we do
        success = False
        match serializer.validated_data['type']:
            case "folder":
                folder_service = FolderService(destination="project", location_id=pk)
                serializer, success = folder_service.update(request)
            case "link":
                link_service = DocumentLinkService(destination="project", location_id=pk)
                serializer, success = link_service.update(request)
            case _:
                document_service = DocumentService(destination="project", location_id=pk)
                serializer, success = document_service.update(request)

        # Update the data
        if success:
            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['GET'],
        detail=True,
        url_path='groups'
    )
    def groups_list(self, _, pk, *args, **kwargs):
        group_service = GroupService(destination="project", location_id=pk)
        serializer = group_service.get_list(_)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @groups_list.mapping.post
    def groups_list_create(self, request, pk, *args, **kwargs):
        # Create new connection first
        group_service = GroupService(destination="project", location_id=pk)
        serializer, success = group_service.create(request)

        # Check results
        if not success:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Utilise get list method and send back the complete list
        serializer = group_service.get_list(request)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'groups/(?P<group_pk>[^/.]+)'
    )
    def groups_list_delete(self, request, pk, group_pk, *args, **kwargs):
        # Delete group
        group_service = GroupService(destination="project", location_id=pk)

        # If you can not delete - notify user
        if not group_service.delete(request, group_pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Return complete list
        # Utilise get list method and send back the complete list
        serializer = group_service.get_list(request)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['GET'],
        detail=True,
        url_path='link_list'
    )
    def link_list(self, _, pk, *args, **kwargs):
        link_list_service = LinkListService(destination="project", location_id=pk)
        serializer = link_list_service.get_list(_)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @link_list.mapping.post
    def link_list_create(self, request, pk, *args, **kwargs):
        link_list_service = LinkListService(destination="project", location_id=pk)
        serializer, success = link_list_service.create(request)

        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'link_list/(?P<link_pk>[^/.]+)'
    )
    def link_list_delete(self, request, pk, link_pk, *args, **kwargs):
        link_list_service = LinkListService(destination="project", location_id=pk)

        if link_list_service.delete(request, link_pk):
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    @destination_permission(min_permission_level=1)
    @link_list_delete.mapping.patch
    def link_list_update(self, request, pk, link_pk, *args, **kwargs):
        link_list_service = LinkListService(destination="project", location_id=pk)

        # Update the data
        serializer, success = link_list_service.update(request, link_pk)
        if success:
            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        object_assignment_results = ObjectAssignment.objects.filter(
            project_id__isnull=False,
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            )
        )

        project_results = Project.objects.filter(
            is_deleted=False,
            id__in=object_assignment_results.values("project_id"),
        )

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search is not None:
            # Translate search to id
            search_id = int(search) if str.isdigit(search) else None

            # Apply search filter
            project_results = project_results.filter(
                Q(title__icontains=search) |
                Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            project_results = project_results.exclude(
                status__higher_order_status="Closed",
            )

        # Handle pagination
        page = self.paginate_queryset(project_results)
        if page is not None:
            serializer = ProjectSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback method
        serializer = ProjectSerializer(
            project_results,
            many=True,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['GET'],
        detail=True,
        url_path='notes',
    )
    def notes(self, _, pk, *args, **kwargs):
        note_service = NoteService(destination="project", location_id=pk)

        # Get data
        serialize = note_service.get_all_notes()

        # Return data
        return Response(
            data=serialize.data,
            status=status.HTTP_200_OK,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['POST'],
        detail=True,
        url_path='notes',
    )
    def notes_create(self, request, pk):
        note_service = NoteService(destination="project", location_id=pk)

        # Create note
        serializer, success = note_service.create_note(request)
        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=2)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'notes/(?P<note_pk>[^/.]+)'
    )
    def notes_delete(self, request, pk, note_pk):
        note_service = NoteService(destination="project", location_id=pk)

        # Delete notes
        success = note_service.delete(request, note_pk)
        if success:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=2)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'notes/(?P<note_pk>[^/.]+)'
    )
    def notes_update(self, request, pk, note_pk):
        note_service = NoteService(destination="project", location_id=pk)

        # Update notes
        serializer, success = note_service.update_note(request, note_pk)

        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['POST'],
        detail=True,
        url_path='organisation',
    )
    def organisation(self, request, pk, *args, **kwargs):
        organisation_service = OrganisationService(destination="project", location_id=pk)

        # Create Link
        serializer, success = organisation_service.link_organisation(request)
        if success:
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @destination_permission(min_permission_level=1)
    @organisation.mapping.delete
    def organisation_delete(self, _, pk, *args, **kwargs):
        organisation_service = OrganisationService(destination="project", location_id=pk)

        # Create Link
        serializer, success = organisation_service.unlink_organisation()
        if success:
            return Response(
                data={},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data=serializer,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, pk, *args, **kwargs):
        project = get_object_or_404(
            Project.objects.filter(is_deleted=False),
            pk=pk
        )
        serializer = ProjectSerializer(
            project,
            data=request.data,
            context={
                'request': request,
                'method': 'PATCH',
            },
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make sure we update the change user
        serializer.change_user = request.user
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, pk, *args, **kwargs):
        project_results = get_object_or_404(
            queryset=Project.objects.filter(is_deleted=False),
            pk=pk,
        )

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            project_id=pk,
        )

        # Define groups list
        project_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values(
                "group_id"
            ),
        )

        # Define user list
        project_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(
            profile_picture=F('userprofilepicture__document_id__key')
        )

        # Create the serializer
        serializer = ProjectSerializer(
            project_results,
            context={
                'request': request,
                'method': 'GET',
            },
        )

        # Append extra data

        return Response(serializer.data)

    @destination_permission(min_permission_level=1)
    @action(
        methods=['POST'],
        detail=True,
        url_path='users'
    )
    def users_list_create(self, request, pk, *args, **kwargs):
        # Create new connection first
        user_service = UserService(destination="project", location_id=pk)
        serializer, success = user_service.create(request)

        # Check results
        if not success:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=status.HTTP_201_CREATED,
        )

    @destination_permission(min_permission_level=1)
    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'users/(?P<user_pk>[^/.]+)'
    )
    def users_list_delete(self, request, pk, user_pk, *args, **kwargs):
        # Delete user
        user_service = UserService(destination="project", location_id=pk)

        # If you can not delete - notify user
        if not user_service.delete(request, user_pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Return complete list
        # Utilise get list method and send back the complete list
        serializer = user_service.get_list(request)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
