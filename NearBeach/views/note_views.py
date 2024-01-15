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

    # Get object note
    form.save()

    return HttpResponse("")
