from NearBeach.models import (
    ObjectNote,
    KanbanCard,
)
from django.db.models import F, Value, Case, When

from NearBeach.serializers.object_data.note_serializer import NoteSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class NoteService(ObjectServiceAbstraction):
    """Service to help create, read, update and delete note objects"""
    def create(self, request):
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # SAVE DATA
        submit_object_note = ObjectNote(
            change_user=request.user,
            object_note=serializer.data["object_note"],
            **{F"{self.destination}_id": self.location_id}
        )

        # When we have a kanban_card as a destination, we want to make sure it isn't a linked object.
        # If it is, we'll need to link the object to the same note
        if self.destination == "kanban_card":
            kanban_card_results = KanbanCard.objects.get(kanban_card_id=self.location_id)

            # Go through each potential object connection
            for object_type in ["project", "task", "requirement"]:
                if not getattr(kanban_card_results, F"{object_type}_id") is None:
                    submit_object_note = submit_object_note.filter(
                        **{F"{object_type}": getattr(kanban_card_results, F"{object_type}_id")}
                    )

        submit_object_note.save()

        # Get the serialized data
        serializer = NoteSerializer(submit_object_note)

        return serializer, True

    def delete(self, request, note_pk: int):
        """Method to delete a note"""
        object_note = ObjectNote.objects.filter(
            is_deleted=False,
            pk=note_pk,
            **{self.destination: self.location_id},
        )

        # If there are no values to update - notify the user
        if len(object_note) == 0:
            return False

        # Soft delete the data
        object_note.update(
            is_deleted=True,
            change_user=request.user,
        )

        return True

    def get_list(self, request):
        """Method to retrieve all notes for an object"""
        note_results = ObjectNote.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        ).annotate(
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
        )

        # Serialise
        return NoteSerializer(note_results, many=True)

    def update(self, request, pk):
        """Method to update a note"""
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Check object exists
        object_note = ObjectNote.objects.get(
            pk=pk,
            is_deleted=False,
            **{self.destination: self.location_id},
        )
        if object_note is None:
            return {"Note object does not exist"}, False

        # TODO - Limit the ability to edit to administrators OR Author of note

        # Update
        object_note.change_user = request.user
        object_note.note = serializer.data["object_note"]
        object_note.save()

        # Serialize
        serializer = NoteSerializer(object_note)

        return serializer, True
