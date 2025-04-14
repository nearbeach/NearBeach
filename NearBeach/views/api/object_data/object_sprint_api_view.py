from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.serializers.object_data.object_sprint_serializer import ObjectSprintSerializer
from NearBeach.models import Sprint


@extend_schema(
    tags=["Object Data|Sprints"]
)
class ObjectSprintViewSet(viewsets.ViewSet):
    serializer_class = ObjectSprintSerializer

    def _get_object_sprint_list(self, destination, location_id):
        # Get data
        sprint_results = Sprint.objects.filter(
            is_deleted=False,
            **{F"{destination}_id": location_id},
        ).values(
            "sprint_id",
            "sprint_name",
            "total_story_points",
            "completed_story_points",
            "sprint_status",
            "sprint_start_date",
            "sprint_end_date",
        )

        # Serialize the data
        return ObjectSprintSerializer(
            sprint_results,
            many=True,
        )

    @api_object_data_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = ObjectSprintSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        sprint_end_date = serializer.data["sprint_end_date"]
        sprint_name = serializer.data["sprint_name"]
        sprint_start_date = serializer.data["sprint_start_date"]

        # Save the data in a new object
        sprint_submit = Sprint(
            sprint_name=sprint_name,
            sprint_start_date=sprint_start_date,
            sprint_end_date=sprint_end_date,
            change_user=request.user,
            **{F"{destination}_id": location_id, },
        )
        sprint_submit.save()

        # Get the update sprint list
        serializer = self._get_object_sprint_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        serializer = ObjectSprintSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the update sprint list
        serializer = self._get_object_sprint_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
