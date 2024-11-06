from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Case, When, Value as V
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from NearBeach.decorators.check_destination import check_destination
from NearBeach.forms import EditNoteForm, AddNoteForm
from NearBeach.models import ObjectNote, KanbanCard
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions, \
    check_user_generic_permissions
from NearBeach.decorators.check_user_permissions.organisation_permissions import check_user_organisation_note_permissions

import json

from NearBeach.views.tools.internal_functions import set_object_from_destination, get_object_from_destination


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
@check_user_generic_permissions(min_permission_level=2, extra_permissions="note")
def add_notes(request, destination, location_id, *args, **kwargs):
    # Add the note, and get the results back
    note_json = generic_add_note(request, destination, location_id)

    return HttpResponse(note_json, content_type="application/json")


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


# INTERNAL FUNCTIONS
def generic_add_note(request, destination, location_id):
    # Fill out the form
    form = AddNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # SAVE DATA
    submit_object_note = ObjectNote(
        change_user=request.user,
        object_note=form.cleaned_data["note"],
    )
    submit_object_note = set_object_from_destination(
        submit_object_note,
        destination,
        location_id
    )

    # When we have a kanban_card as a destination, we want to make sure it isn't a linked object. If it is, we'll need
    # to link the object to the same note
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

    # Get data to send back to user
    note_results = ObjectNote.objects.filter(
        object_note_id=submit_object_note.object_note_id
    )

    note_results = note_results.annotate(
        username=F('change_user'),
        first_name=F('change_user__first_name'),
        last_name=F('change_user__last_name'),
        profile_picture=F('change_user__userprofilepicture__document_id__document_key'),
        can_edit = Case(
            When(change_user=request.user, then=V('true')),
            default=V('false')
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

    # Return JSON results
    return json.dumps(list(note_results), cls=DjangoJSONEncoder)


# INTERNAL FUNCTION
def generic_update_note(request):
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


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
@check_user_generic_permissions(min_permission_level=1)
def note_list(request, destination, location_id, *args, **kwargs):
    # Everyone should have access to the notes section.

    # Get the notes dependent on the user destination and location
    note_results = ObjectNote.objects.filter(
        is_deleted=False,
    )

    # Filter by destination and location_id
    note_results = get_object_from_destination(note_results, destination, location_id)

    # Filter for the fields that we want
    note_results = (note_results.annotate(
        username=F('change_user'),
        first_name=F('change_user__first_name'),
        last_name=F('change_user__last_name'),
        profile_picture=F('change_user__userprofilepicture__document_id__document_key'),
        can_edit=Case(
            When(change_user=request.user, then=V('true')),
            default=V('false')
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
    note_json = json.dumps(list(note_results), cls=DjangoJSONEncoder)

    return HttpResponse(note_json, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
@check_user_organisation_note_permissions()
def organisation_add_notes(request, _, organisation_id, *args, **kwargs):
    # Add the note, and get the results
    note_json = generic_add_note(request, "organisation", organisation_id)

    return HttpResponse(note_json, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="organisation")
def organisation_delete_note(request, object_note_id, *args, **kwargs):
    # Delete all the objects with the id
    ObjectNote.objects.filter(
        object_note_id=object_note_id
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
@check_specific_object_permissions(min_permission_level=1, object_lookup="organisation")
def organisation_note_list(request, _, organisation_id, *args, **kwargs):
    # Filter for the fields that we want
    note_results = ObjectNote.objects.filter(
        is_deleted=False,
        organisation_id=organisation_id,
    ).annotate(
        username=F('change_user'),
        first_name=F('change_user__first_name'),
        last_name=F('change_user__last_name'),
        profile_picture=F('change_user__userprofilepicture__document_id__document_key'),
        can_edit=Case(
            When(change_user=request.user, then=V('true')),
            default=V('false')
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

    # Return JSON results
    note_json = json.dumps(list(note_results), cls=DjangoJSONEncoder)

    return HttpResponse(note_json, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="organisation")
def organisation_update_note(request, *args, **kwargs):
    generic_update_note(request)

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="object_note")
def update_note(request, *args, **kwargs):
    generic_update_note(request)

    return HttpResponse("")
