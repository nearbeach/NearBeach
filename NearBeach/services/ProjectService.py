from NearBeach.models import Project
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.utils.api.check_group_list import check_group_list
from NearBeach.utils.objects.error_object import ErrorObject


class ProjectService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete project objects"""

    def create(self, request):
        """Method for creating a new project"""
        serializer = ProjectSerializer(
            context={
                "request": request,
                "method": "POST",
            },
            data=request.data,
        )
        if not serializer.is_valid():
            return serializer, False

        # Check that there are groups
        # group_list = request.data.getlist("group_list", [])
        group_list = serializer.validated_data["group_list"]
        if not check_group_list(request.user, group_list):
            return ErrorObject("No Access to groups provided"), False

        # Create the project
        created_project = serializer.save(
            change_user=request.user, creation_user=request.user
        )

        # Re-serialize the created project so it is in the same shape for the user
        serializer = ProjectSerializer(created_project, many=False)

        return serializer, True

    def delete(self, request, _):
        project = Project.objects.filter(
            pk=self.location_id,
            is_deleted=False,
        )

        if len(project) == 0:
            return False

        project.update(
            is_deleted=True,
            change_user=request.user,
        )

        return True

    def get_list(self, request):
        pass

    def update(self, request, project_id: int):
        pass
