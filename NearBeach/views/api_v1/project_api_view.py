from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.models import Project, ObjectAssignment, UserGroup
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.utils.api.check_group_list import check_group_list


@extend_schema(
    tags=["Projects"],
    methods=["GET", "POST", "PATCH", "DELETE"],
)
class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs):
        serializer = ProjectSerializer(
            context={'request': request},
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
                "Groups are missing",
                status=status.HTTP_400_BAD_REQUEST,
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

    @staticmethod
    @destination_permission(min_permission_level=1)
    def list(request, *args, **kwargs):
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

        # Handle pagination
        # page = self.paginate_queryset(project_results)
        # if page is not None:
        #     serializer = ProjectSerializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = ProjectSerializer(
            data=project_results,
            many=True
        )

        serializer.is_valid(raise_exception=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, teapot can not be upgraded to coffee pot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, I'm a teapot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )
