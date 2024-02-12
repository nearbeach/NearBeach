from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

from NearBeach.forms import EditNoteForm
from NearBeach.models import ObjectNote
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="object_note")
def delete_note(request, object_note_id, *args, **kwargs):
    # Delete all the objects with the id
    ObjectNote.objects.filter(
        object_note_id=object_note_id
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="object_note")
def update_note(request, object_note_id, *args, **kwargs):
    # Check the form
    form = EditNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the object to update
    update_object_note = ObjectNote.objects.get(
        object_note_id=form.cleaned_data["object_note_id"],
    )

    # Update the data
    update_object_note.object_note = form.cleaned_data["object_note"]
    update_object_note.change_user = request.user
    update_object_note.save()

    return HttpResponse("")
