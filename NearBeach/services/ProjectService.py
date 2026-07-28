from typing import Tuple, Union, Dict

from rest_framework import status

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q, F

from NearBeach.models import Project, ObjectAssignment, UserGroup, Group
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.utils.api.check_group_list import check_group_list
from NearBeach.utils.api.check_object_exists import check_object_exists


class ProjectService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete project objects"""

    def create(self, request) -> Tuple[Union[Dict, str], int]:
        """Method for creating a new project"""
        serializer = ProjectSerializer(
            context={
                "request": request,
                "method": "POST",
            },
            data=request.data,
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check that there are groups
        group_list = serializer.validated_data["group_list"]
        if not check_group_list(request.user, group_list):
            return "No Access to groups provided", status.HTTP_400_BAD_REQUEST

        # Create the project
        created_project = serializer.save(
            change_user=request.user, creation_user=request.user
        )

        # Re-serialize the created project so it is in the same shape for the user
        serializer = ProjectSerializer(created_project, many=False)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, _) -> int:
        project = Project.objects.filter(
            pk=self.location_id,
            is_deleted=False,
        )

        if len(project) == 0:
            return status.HTTP_400_BAD_REQUEST

        project.update(
            is_deleted=True,
            change_user=request.user,
        )

        return status.HTTP_204_NO_CONTENT

    def get_list(self, request) -> QuerySet:
        object_assignment_results = ObjectAssignment.objects.filter(
            project_id__isnull=False,
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            ),
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
                Q(title__icontains=search) | Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            project_results = project_results.exclude(
                status__higher_order_status="Closed",
            )

        return project_results

    def retrieve(self, request) -> Tuple[Union[Dict, str], int]:
        """Method used to retrieve a single project"""
        if not check_object_exists(self.destination, self.location_id):
            return "Object does not exist", status.HTTP_400_BAD_REQUEST

        # Get object
        project_results = Project.objects.get(pk=self.location_id)

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            project_id=self.location_id,
        )

        # Define groups list
        project_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values("group_id"),
        )

        # Define user list
        project_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = ProjectSerializer(
            project_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request, _) -> Tuple[Union[Dict, str], int]:
        if not check_object_exists(self.destination, self.location_id):
            return "Object does not exist", status.HTTP_400_BAD_REQUEST

        # Get project
        project = Project.objects.get(pk=self.location_id)

        # Setup serializer
        serializer = ProjectSerializer(
            project,
            data=request.data,
            context={
                "request": request,
                "method": "PATCH",
            },
            partial=True,
        )
        if not serializer.is_valid():
            return serializer.errors, False

        # Make sure we update the change user
        serializer.change_user = request.user
        serializer.save()

        return serializer.data, status.HTTP_200_OK
