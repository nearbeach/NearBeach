from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import F, Case, When, Value

from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.serializers.object_data.note_serializer import NoteSerializer
from NearBeach.models import (
    KanbanCard,
    ObjectNote,
)
from NearBeach.views.tools.internal_functions import set_object_from_destination

#TODO - double check the permissions for the Notes API. Do we use special permissions?
#NOTE - We might need to have a custom permissions, for the organisation vs other objects. This needs testing


@extend_schema(
    tags=["Object Data|Notes"]
)
class NoteViewSet(viewsets.ViewSet):
    serializer_class = NoteSerializer

    def _get_list(self, request, destination, location_id):
        # Get the notes dependent on the user destination and location
        note_results = ObjectNote.objects.filter(
            is_deleted=False,
            **{F"{destination}_id": location_id},
        )

        # Filter for the fields that we want
        note_results = (note_results.annotate(
            username=F('change_user'),
            first_name=F('change_user__first_name'),
            last_name=F('change_user__last_name'),
            profile_picture=F('change_user__userprofilepicture__document_id__document_key'),
            can_edit=Case(
                When(change_user=request.user, then=Value('true')),
                default=Value('false')
            )
        ).values(
            "object_note_id",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "object_note",
            "date_modified",
            "can_edit",
        ))

        # Return JSON results
        return NoteSerializer(
            note_results,
            many=True,
        )

    @extend_schema(
        description="""
# 📌 Description

Create a note against the current object

# 🧾 Parameters

- Object Note: The new note
- destination - the object of choice. Choices are;
    - Kanban Card
    - Organisation
    - Requirement
    - Requirement Item
    - Project
    - Task
- location id - the id of the object
""",
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new kanban board",
                value={
                    "kanban_board_name": "My Kanban Board",
                    "group_list": [1, 2],
                    "kanban_column": [
                        {
                            "kanban_column_name": "Backlog",
                            "kanban_column_property": "Backlog",
                        },
                        {
                            "kanban_column_name": "Blocked",
                            "kanban_column_property": "Blocked",
                        },
                        {
                            "kanban_column_name": "In Progress",
                            "kanban_column_property": "Normal",
                        },
                        {
                            "kanban_column_name": "User Acceptance Testing",
                            "kanban_column_property": "Normal",
                        },
                        {
                            "kanban_column_name": "Closed",
                            "kanban_column_property": "Closed",
                        },
                    ],
                    "kanban_level": [
                        {
                            "kanban_level_name": "Swimlane 1",
                        },
                        {
                            "kanban_level_name": "Swimlane 2",
                        },
                    ],
                }
            )
        ],
    )
    @api_object_data_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = NoteSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        object_note = serializer.data["object_note"]

        # SAVE DATA
        submit_object_note = ObjectNote(
            change_user=request.user,
            object_note=object_note,
            **{F"{destination}_id": location_id}
        )

        # When we have a kanban_card as a destination, we want to make sure it isn't a linked object.
        # If it is, we'll need to link the object to the same note
        if destination == "kanban_card":
            kanban_card_results = KanbanCard.objects.get(kanban_card_id=location_id)

            # Go through each potential object connection
            for object_type in ["project", "task", "requirement"]:
                if not getattr(kanban_card_results, F"{object_type}_id") is None:
                    submit_object_note = set_object_from_destination(
                        submit_object_note,
                        object_type,
                        getattr(kanban_card_results, F"{object_type}_id"),
                    )

        submit_object_note.save()

        # Get the serialized data
        serializer = self._get_list(request, destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        description="""
# 📌 Description


Deletes a single note. You can get the note id from the list
    """
    )
    @api_object_data_permissions(min_permission_level=2)
    def destroy(self, request, pk=None, *args, **kwargs):
        serializer = NoteSerializer(
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

        # Get the note to delete
        delete_note = ObjectNote.objects.filter(
            object_note_id=pk,
            is_deleted=False,
            **{F"{destination}_id": location_id},
        )

        if len(delete_note) == 0:
            return Response(
                data={"No notes to delete"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        delete_note.update(
            is_deleted=True,
            change_user=request.user,
        )

        # Get the serialized data
        serializer = self._get_list(request, destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        description="""
# 📌 Description

Gathers a list of notes assigned to the current object


# 🧾 Parameters

- destination - the object of choice. Choices are;
    - Kanban Card
    - Organisation
    - Requirement
    - Requirement Item
    - Project
    - Task
- location id - the id of the object
        """,
    )
    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        serializer = NoteSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Variables
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the serialized data
        serializer = self._get_list(request, destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="""
# 📌 Description

Updates a single note under an object

# 🧾 Parameters
- Object Note: The new note
- destination - the object of choice. Choices are;
    - Kanban Card
    - Organisation
    - Requirement
    - Requirement Item
    - Project
    - Task
- location id - the id of the object
    """
    )
    @api_object_data_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = NoteSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the object to update
        update_object_note = get_object_or_404(
            queryset=ObjectNote.objects.filter(
                is_deleted=False,
            ),
            pk=pk,
        )

        serializer.update(
            update_object_note,
            serializer.data,
        )

        # Get the serialized data
        serializer = self._get_list(
            request,
            kwargs["destination"],
            kwargs["location_id"]
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
