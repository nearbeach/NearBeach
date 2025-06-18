from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import F

from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.serializers.object_data.tag_serializer import TagSerializer
from NearBeach.models import Tag, TagAssignment


@extend_schema(
    tags=["Object Data|Tags"]
)
class TagViewSet(viewsets.ViewSet):
    serializer_class = TagSerializer
    
    @staticmethod
    def _get_tag_list(destination, location_id):
        # Get the data we want
        tag_results = TagAssignment.objects.filter(
            is_deleted=False,
            tag_id__is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        ).annotate(
            tag_name=F("tag_id__tag_name"),
            tag_colour=F("tag_id__tag_colour"),
            tag_text_colour=F("tag_id__tag_text_colour"),
        ).values(
            "tag_assignment_id",
            "tag_id",
            "tag_name",
            "tag_colour",
            "tag_text_colour",
        )

        return TagSerializer(
            tag_results,
            many=True,
        )

    @extend_schema(
        description="""
# 📌 Description

This endpoint allows you to add a tag to the specific object

# 🧾 Parameters

- Destination: The type of object you're linking to. Must be one of the following:
    - Kanban Card
    - Project
    - Request for Change
    - Requirement
    - Requirement Item
    - Task
- Location ID: The unique ID of the specific object you're modifying (e.g., the project ID or task ID).
- tag_list: A list of ID's connected to the tags. You can fet all tag data by hitting the available data tag list.
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Add Tag Id of 1 to current project. Url is `api/v0/project/2/tag/`",
                value={"tag_id": [1]},
            ),
        ],
    )
    @api_object_data_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = TagSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        tag_list = serializer.data["tag_list"]

        for single_tag in tag_list:
            # Grab the tag instance
            tag_instance = Tag.objects.get(tag_id=single_tag)

            submit_tag_assignment = TagAssignment(
                tag=tag_instance,
                object_enum=destination,
                object_id=location_id,
                change_user=request.user,
            )
            submit_tag_assignment.save()

        # Get updated list
        serializer = self._get_tag_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        description="""
# 📌 Description

Destroy a tag connected against the current object

# 🧾 Parameters

- Destination: The type of object you're linking to. Must be one of the following:
    - Kanban Card
    - Project
    - Request for Change
    - Requirement
    - Requirement Item
    - Task
- Location ID: The unique ID of the specific object you're modifying (e.g., the project ID or task ID).
- Tag Id: this can be found out using the list functionality.
        """,
    )
    @api_object_data_permissions(min_permission_level=2)
    def destroy(self, request, pk=None, *args, **kwargs):
        serializer = TagSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the tags to delete
        remove_tag = TagAssignment.objects.filter(
            tag_assignment_id=pk,
            is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        )

        if len(remove_tag) == 0:
            return Response(
                data={"No tags to delete"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Delete the tags
        remove_tag.update(
            is_deleted=True,
            change_user=request.user,
        )

        return Response(
            data={"Tag has been removed from object"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all tags currently under the object

# 🧾 Parameters

- Destination: The type of object you're linking to. Must be one of the following:
    - Kanban Card
    - Project
    - Request for Change
    - Requirement
    - Requirement Item
    - Task
- Location ID: The unique ID of the specific object you're modifying (e.g., the project ID or task ID).
        """,
    )
    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        serializer = TagSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the serialized data
        serializer = self._get_tag_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
