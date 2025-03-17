from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    ObjectAssignment,
    Organisation,
    Project, UserGroup,
)
from NearBeach.serializers.project_serializer import ProjectSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads


class ProjectViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer

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

        # Gather instances
        organisation_instance = Organisation.objects.get(
            organisation_id=serializer.data.get("organisation_id"),
        )

        # Get first project status
        project_status = ListOfProjectStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "project_status_sort_order",
        )

        project_submit = Project(
            project_name=serializer.data.get("project_name"),
            project_description=serializer.data.get("project_description"),
            organisation=organisation_instance,
            project_start_date=serializer.data.get("project_start_date"),
            project_end_date=serializer.data.get("project_end_date"),
            project_status=project_status.first(),
            change_user=request.user,
            creation_user=request.user,
        )
        project_submit.save()

        # Assign project to the groups
        for single_group in group_list:
            group_instance = Group.objects.get(
                group_id=single_group,
            )

            # Save the group against the new project
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                project=project_submit,
                change_user=request.user,
            )
            submit_object_assignment.save()

        # Transfer any images to the new project id
        transfer_new_object_uploads(
            "project",
            project_submit.project_id,
            serializer.data.get("uuid")
        )

        return Response(
            data={ "project_id": project_submit.project_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.change_user = request.user
        project.save()
        return Response(data='project deleted')

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
        )[(page - 1) * page_size : page * page_size]

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

        # Obtain Instances
        project_status_instance = ListOfProjectStatus.objects.get(
            project_status_id=serializer.data["project_status"],
        )

        # Update Project
        update_project = Project.objects.get(pk=pk)
        update_project.project_name = serializer.data["project_name"]
        update_project.project_description = serializer.data["project_description"]
        update_project.project_start_date = serializer.data["project_start_date"]
        update_project.project_end_date = serializer.data["project_end_date"]
        update_project.project_status = project_status_instance
        update_project.project_priority = serializer.data["project_priority"]
        update_project.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

