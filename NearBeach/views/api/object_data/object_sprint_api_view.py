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

    @staticmethod
    def _get_object_sprint_list(destination, location_id):
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

    @extend_schema(
        description="""
# 📌 Description

Create Kanban Card against the kanban board.

# 🧾 Parameters

- **Destination**: The type of object you are querying. Must be one of:
  - Kanban Card  
  - Project  
  - Request for Change  
  - Requirement  
  - Requirement Item  
  - Task  

- **Location ID**: The unique ID of the specific object instance.
- **Sprint End Date**: End date of the sprint
- **Sprint Start Date**: Start date of the sprint
- **Sprint Name**: Sprint Name

# ✅ Notes

Both the Column/Level id's will need to exist under the current kanban board. Or an error will occur.
        """,
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

        serializer.save(
            change_user=request.user,
            destination=destination,
            location_id=location_id
        )

        # Send back all the sprint list
        serializer = self._get_object_sprint_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

List all the sprints currently connected to the object
        """
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
