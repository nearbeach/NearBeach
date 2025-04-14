from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.db.models import Q

from NearBeach.models import (
    ObjectAssignment,
    Sprint,
    UserGroup,
)
from NearBeach.serializers.available_data.sprint_list_serializer import SprintListSerializer


@extend_schema(
    tags=["Available Data"]
)
class SprintListViewSet(viewsets.ViewSet):
    serializer_class = SprintListSerializer

    #TODO: Check to see if we need to implement permissions
    def list(self, request, *args, **kwargs):
        object_assignment_results = ObjectAssignment.objects.filter(
            Q(
                is_deleted=False,
                group_id__in=UserGroup.objects.filter(
                    is_deleted=False,
                    username=request.user,
                ).values('group_id'),
            ) & Q(
                Q(project_id__isnull=False) |
                Q(requirement_id__isnull=False)
            )
        )

        # Using the object assignment results - we can determine which sprints the user has access too
        sprint_results = Sprint.objects.filter(
            Q(
                is_deleted=False,
                project_id__in=object_assignment_results.values("project_id"),
            ) |
            Q(
                is_deleted=False,
                requirement_id__in=object_assignment_results.values("requirement_id"),
            )
        ).exclude(
            sprint_status="Finished",
        )

        serializer = SprintListSerializer(
            sprint_results,
            many=True,
        )

        return Response(serializer.data)
