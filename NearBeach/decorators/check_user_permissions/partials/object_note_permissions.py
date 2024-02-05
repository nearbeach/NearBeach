from NearBeach.models import ObjectAssignment, ObjectNote, UserGroup
from django.db.models import Max, Q


def object_note_permissions(request, kwargs):
    """
    Checks the user's permission to determine if they have permission to delete this note.
    Currently only;
    - Note owner
    Can delete the note
    """

    if len(kwargs) > 0:
        # Get the requirement groups
        object_results = ObjectNote.objects.filter(
            object_note_id=kwargs["object_note_id"],
            change_user=request.user,
        ).count()

        return True, object_results

    return False, 0
