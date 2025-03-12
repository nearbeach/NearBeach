from NearBeach.decorators.check_user_permissions.object_permissions import check_user_generic_permissions
from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    ObjectAssignment,
    Organisation,
    Project,
)
from NearBeach.serializers.project_serializer import ProjectSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import permissions, renderers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from NearBeach.views.document_views import transfer_new_object_uploads


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'project': reverse('project-list', request=request, format="json"),
        # 'users': reverse('user-list', request=request, format=format),
        # 'snippets': reverse('snippet-list', request=request, format=format)
    })


class ProjectViewSet(viewsets.ModelViewSet):
    # Check User Authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    # Setup the queryset and serialiser class
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer

    # @check_user_generic_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
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
        group_list = serializer.data.get("group_list")
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

        return Response(serializer.data)

    @check_user_generic_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.change_user = request.user
        project.save()
        return Response(data='project deleted')

