from rest_framework.generics import get_object_or_404

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


class SprintViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Sprint.objects.filter(is_deleted=False)
    serializer_class = SprintSerializer

    @check_api_sprint_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack values
        destination = serializer.data.get("destination")
        location_id = serializer.data.get("location_id")

        # Save the data
        sprint_submit = Sprint(
            sprint_name=serializer.data.get("sprint_name"),
            sprint_start_date=serializer.data.get("sprint_start_date"),
            sprint_end_date=serializer.data.get("sprint_end_date"),
            change_user=request.user,
            **{F"{destination}_id": location_id},
        )
        sprint_submit.save()

        return Response(
            data={ "sprint_id": sprint_submit.sprint_id },
            status=status.HTTP_201_CREATED,
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

        # Get variables
        destination = serializer.data.get("destination")
        location_id = serializer.data.get("location_id")

        delete_sprint = Sprint.objects.filter(
            sprint_id=pk,
            is_deleted=False,
            **{F"{destination}_id": location_id},
        )

        if len(delete_sprint) == 0:
            return Response(
                data={"No sprints to delete"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        delete_sprint.update(
            is_deleted=True,
            change_user=request.user,
        )

        return Response(data='sprint deleted')

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
        )[(page - 1) * page_size : page * page_size]

        serializer = SprintSerializer(sprint_results, many=True)

        return Response(serializer.data)

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

    @check_sprint_permission_with_sprint(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flat pack variables
        destination = serializer.data.get("destination")
        location_id = serializer.data.get("location_id")

        # Update Sprint
        update_sprint = Sprint.objects.filter(
            pk=pk,
            is_deleted=False,
            **{F"{destination}_id": location_id},
        )
        if len(update_sprint) == 0:
            return Response(
                data={"Sprint not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update sprint
        update_sprint = update_sprint[0]
        update_sprint.sprint_name = serializer.data.get("sprint_name")
        update_sprint.sprint_start_date = serializer.data.get("sprint_start_date")
        update_sprint.sprint_end_date = serializer.data.get("sprint_end_date")
        update_sprint.save()

        sprint_results = Sprint.objects.get(pk=pk)
        sprint_results.destination = serializer.data.get("destination")
        sprint_results.location_id = serializer.data.get("location_id")
        serializer = SprintSerializer(sprint_results)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
