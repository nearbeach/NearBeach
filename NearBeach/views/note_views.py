from django.http import HttpResponse, HttpResponseBadRequest

from NearBeach.forms import DeleteNoteForm, EditNoteForm
from NearBeach.models import ObjectNote


def delete_note(request):
    # Check the form
    form = DeleteNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Delete all the objects with the id
    ObjectNote.objects.filter(
        object_note_id=form.cleaned_data["object_note_id"],
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


def update_note(request):
    # Check the form
    form = EditNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the object to update
    update_object_note = ObjectNote.objects.get(
        object_note_id=form.cleaned_data["object_note_id"],
    )

    # Update the data
    update_object_note.object_note=form.cleaned_data["object_note"]
    update_object_note.change_user=request.user
    update_object_note.save()

    return HttpResponse("")
