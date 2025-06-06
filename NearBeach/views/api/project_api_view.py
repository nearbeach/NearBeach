from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    ObjectAssignment,
    Organisation,
    Project,
    UserGroup,
)
from NearBeach.serializers.project_serializer import ProjectSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads


@extend_schema(
    tags=["Projects"]
)
class ProjectViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer

    @extend_schema(
        description="""
# 📌 Description

This endpoint allows you to add a project within NearBeach.
        """
    )
    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        group_list = request.data.getlist('group_list', [])
        if group_list is None or len(group_list) == 0:
            return Response(
                "Groups are missing",
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_project = serializer.save(change_user=request.user, creation_user=request.user)

        # Transfer any images to the new project id
        transfer_new_object_uploads(
            "project",
            serializer.data.get("project_id"),
            serializer.data.get("uuid")
        )

        # Re-serialize the created project so it is in the same shape for the user
        serializer = ProjectSerializer(created_project, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.change_user = request.user
        project.save()
        return Response(
            data='project deleted',
            status=status.HTTP_204_NO_CONTENT,
        )

    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Setup Attributes
        page_size = int(request.query_params.get("page_size", 100))
        page_size = page_size if page_size <= 1000 else 1000
        page = int(request.query_params.get("page", 1))

        object_assignment_results = ObjectAssignment.objects.filter(
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
            project_id__in=object_assignment_results.values("project_id"),
        # )[(page - 1) * page_size : page * page_size]
        )

        serializer = ProjectSerializer(project_results, many=True)

        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Project.objects.all()
        project_results = get_object_or_404(
            queryset,
            pk=pk
        )
        serializer = ProjectSerializer(project_results)
        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # serializer.save(change_user=request.user)
        update_project = Project.objects.get(pk=pk)
        update_project = serializer.update(
            update_project,
            serializer.data
        )

        # Re-serialize the data to send back complete set to user
        serializer = ProjectSerializer(
            update_project,
            many=False
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

