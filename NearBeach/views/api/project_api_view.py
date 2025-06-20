from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    ObjectAssignment,
    Project,
    UserGroup,
)
from NearBeach.serializers.project_serializer import ProjectSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads


@extend_schema(
    tags=["Projects"],
    methods=["GET", "POST", "PUT", "DELETE"],
)
class ProjectViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        description="""
# 📌 Description

Create Projects to help manage your projects.

# 🧾 Parameters

- Project Name: The project's name. Should be short and under 255 characters.
- Project Description: The description of the project. Can have basic HTML
- Project Start Date
- Project End Date
- Organisation: The organisation that the project belongs too. Should be an int. Use the Organisation API to find the 
correct organisation id.
- Group List: All groups associated with this project. At least one of the user's groups will need to be included. The 
group id's can be found using the Group List API.
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new project",
                value={
                    "project_name": "My Project",
                    "project_description": "<h1>Hello World</h1>",
                    "project_start_date": "2024-12-19 15:49:37",
                    "project_end_date": "2024-12-19 15:49:37",
                    "organisation": 2,
                    "group_list": [1, 2],
                }
            )
        ],
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

        created_project = serializer.save(
            change_user=request.user,
            creation_user=request.user
        )

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

    @extend_schema(
        description="""
# 📌 Description
        
Delete projects.


# ✅ Notes

Users will need to have the permission to delete.
        """
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

    @extend_schema(
        description="""
# 📌 Description

Lists all projects within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?Page=` to navigate to the appropriate page.
    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
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
        )

        # Handle pagination
        page = self.paginate_queryset(project_results)
        if page is not None:
            serializer = ProjectSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProjectSerializer(project_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single project.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Project.objects.filter(
            is_deleted=False,
        )
        project_results = get_object_or_404(
            queryset,
            pk=pk
        )
        serializer = ProjectSerializer(project_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single project.

# 🧾 Parameters

- Project Name: The project's name. Should be short and under 255 characters.
- Project Description: The description of the project. Can have basic HTML
- Project Start Date
- Project End Date
- Project Status: The status of the project.
- Project Priority: The priority of the project.
    - 0 = Highest
    - 1 = High
    - 2 = Normal
    - 3 = Low
    - 4 = Lowest
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Double check the project exists
        queryset = Project.objects.filter(
            is_deleted=False,
        )
        update_project = get_object_or_404(
            queryset,
            pk=pk
        )
        update_project.change_user = request.user
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

