from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from NearBeach.decorators.check_user_permissions.api_sprint_permissions_v0 import check_api_sprint_permissions
from NearBeach.decorators.check_user_permissions.sprint_permissions import check_sprint_permission_with_sprint
from NearBeach.models import (
    ObjectAssignment,
    Sprint,
    UserGroup,
)
from NearBeach.serializers.sprint_serializer import SprintSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, F
import datetime


@extend_schema(
    tags=["Sprint"]
)
class SprintViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Sprint.objects.filter(is_deleted=False)
    serializer_class = SprintSerializer

    @extend_schema(
        description="""
# 📌 Description

Create Sprints to help manage projects/requirements.

# 🧾 Parameters

- Sprint Name: Name of the sprint
- Destination: The object the sprint will be connected too. Either Project or Destination.
- Location ID: The object's ID that the sprint will be connected to
- Sprint Start Date: Start date of the sprint
- Sprint End Date: End date of the sprint
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new project",
                value={
                    "sprint_name": "Hello Sprint",
                    "destination": "project",
                    "location_id": 2,
                    "sprint_start_date": "2024-12-19 15:49:37",
                    "sprint_end_date": "2024-12-19 15:49:37",
                }
            )
        ],
    )
    @check_api_sprint_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the sprint
        sprint_submit = serializer.save(
            change_user=request.user,
        )

        # Re-add the destination back for the serializer
        if sprint_submit.project is not None:
            sprint_submit.destination = "project"
            sprint_submit.location_id = sprint_submit.project_id

        if sprint_submit.requirement is not None:
            sprint_submit.destination = "requirement"
            sprint_submit.location_id = sprint_submit.requirement_id

        # Re-serialize the data
        serializer = SprintSerializer(
            sprint_submit,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete sprints.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_sprint_permission_with_sprint(min_permission_level=4)
    def destroy(self, request, pk=None, *args, **kwargs):
        serializer = SprintSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        delete_sprint = get_object_or_404(
            queryset=Sprint.objects.filter(
                is_deleted=False,
                **{F"{serializer.data.get('destination')}_id": serializer.data.get("location_id")},
            ),
            pk=pk,
        )

        delete_sprint.is_deleted=True
        delete_sprint.change_user=request.user
        delete_sprint.save()

        return Response(
            data='sprint deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all sprints within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?Page=` to navigate to the appropriate page.
    """
    )
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

        sprint_results = Sprint.objects.filter(
            Q(
                is_deleted=False,
                project_id__in=object_assignment_results.filter(
                    project_id__isnull=False,
                ).values(
                    "project_id"
                ),
            ) |
            Q(
                is_deleted=False,
                requirement_id__in=object_assignment_results.filter(
                    requirement_id__isnull=False,
                ).values(
                    "requirement_id"
                ),
            )
        ).annotate(
            destination=Case(
                When(project_id__isnull=False, then=Value("project")),
                When(requirement_id__isnull=False, then=Value("requirement")),
                default=Value("")
            ),
            location_id=Case(
                When(project_id__isnull=False, then=F("project_id")),
                When(requirement_id__isnull=False, then=F("requirement_id")),
                default=Value(0)
            )
        )

        # Handle pagination
        page = self.paginate_queryset(sprint_results)
        if page is not None:
            serializer = SprintSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SprintSerializer(sprint_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single sprint.

    """
    )
    @check_sprint_permission_with_sprint(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Sprint.objects.all()
        sprint_results = get_object_or_404(
            queryset,
            pk=pk
        )

        if sprint_results.project is not None:
            sprint_results.destination = "project"
            sprint_results.location_id = sprint_results.project_id

        if sprint_results.requirement is not None:
            sprint_results.destination = "requirement"
            sprint_results.location_id = sprint_results.requirement_id

        serializer = SprintSerializer(sprint_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single sprint.

# 🧾 Parameters

- Sprint Name: Name of the sprint
- Destination: The object the sprint will be connected too. Either Project or Destination.
- Location ID: The object's ID that the sprint will be connected to
- Sprint Start Date: Start date of the sprint
- Sprint End Date: End date of the sprint
    """
    )
    @check_sprint_permission_with_sprint(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        update_sprint = get_object_or_404(
            queryset=Sprint.objects.filter(
                is_deleted=False,
                **{F"{serializer.data.get('destination')}_id": serializer.data.get("location_id")},
            ),
            pk=pk,
        )
        
        # Update sprint
        update_sprint = serializer.update(update_sprint, serializer.validated_data)

        # Re-serialize the sprint data
        update_sprint.destination = serializer.data.get("destination")
        update_sprint.location_id = serializer.data.get("location_id")
        serializer = SprintSerializer(update_sprint)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
