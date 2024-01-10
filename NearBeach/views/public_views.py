from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect
from django.template import loader
from django.db.models import F

from NearBeach.decorators.check_destination import check_destination, check_public_destination
from NearBeach.views.object_data_views import set_object_from_destination, get_object_from_destination
from NearBeach.models import KanbanCard, \
    KanbanColumn, \
    KanbanLevel, \
    PublicLink, \
    RequirementItem, \
    ListOfProjectStatus, \
    ListOfRequirementItemStatus, \
    ListOfRequirementItemType, \
    ListOfRequirementStatus, \
    ListOfRequirementType, \
    ListOfTaskStatus
from NearBeach.forms import PublicLinkDeleteForm, PublicLinkUpdateForm
from NearBeach.views.kanban_views import get_context as kanban_get_context

import json

# Convert kanban card priorty to dict for easy lookup
from NearBeach.models import KANBAN_CARD_PRIORITY
DICT_KANBAN_CARD_PRIORITY = dict(KANBAN_CARD_PRIORITY)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@csrf_protect
@check_destination()
def create_public_link(request, destination, location_id):
    # Create new public link
    submit_public_link = PublicLink(
        change_user=request.user,
        creation_user=request.user,
    )

    # Assign to the destination/location
    submit_public_link = set_object_from_destination(
        submit_public_link, destination, location_id
    )

    # Save
    submit_public_link.save()

    # Return the data we have
    public_link_results = get_public_link_results(destination, location_id)

    return HttpResponse(
        public_link_results,
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def delete_public_link(request, destination, location_id):
    form = PublicLinkDeleteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the data we want
    uuid = str(form.cleaned_data["public_link_id"])
    public_link_update = PublicLink.objects.filter(
        public_link_id=uuid,
        is_deleted=False,
    )
    public_link_update = get_object_from_destination(public_link_update, destination, location_id)

    public_link_update.update(
        is_deleted=True
    )

    return HttpResponse()


# Internal function
def get_public_context(results):
    organisation_results = getattr(
        results,
        "organisation"
    )

    # Serialise in the if statement - as None can not be serialized
    organisation_results = serializers.serialize("json", [organisation_results])
    results = serializers.serialize("json", [results])

    return {
        "organisation_results": organisation_results,
        "results": results,
    }


# Internal function
def get_public_context_kanban_card(results):
    return {
        "card_column": results.kanban_column.kanban_column_name,
        "card_description": results.kanban_card_description,
        "card_id": results.kanban_card_id,
        "card_level": results.kanban_level.kanban_level_name,
        "card_priority": DICT_KANBAN_CARD_PRIORITY[results.kanban_card_priority],
        "card_text": results.kanban_card_text,
    }


# Internal function
def get_public_context_kanban_board(results):
    # Use the kanban view get_context
    context = kanban_get_context(results.kanban_board_id)

    # Get kanban card results
    kanban_card_results = KanbanCard.objects.filter(
        is_archived=False,
        is_deleted=False,
        kanban_board_id=results.kanban_board_id,
    ).order_by("kanban_card_sort_number")

    # Add kanban card results to context
    context["kanban_card_results"] = serializers.serialize("json", kanban_card_results)

    return context


# Internal function
def get_public_context_project(results):
    # Grab all the status options for the project. Shape the data into the required shape for frontend
    status_options = ListOfProjectStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F('project_status_id'),
        label=F('project_status'),
    ).values(
        "value",
        "label",
        "project_higher_order_status",
    ).order_by(
        "project_status_order"
    )

    organisation_results = getattr(
        results,
        "organisation"
    )

    # Serialise in the if statement - as None can not be serialized
    organisation_results = serializers.serialize("json", [organisation_results])
    results = serializers.serialize("json", [results])

    return {
        "organisation_results": organisation_results,
        "results": results,
        "status_options": json.dumps(list(status_options), cls=DjangoJSONEncoder),
    }

# Internal function
def get_public_context_requirement(results):
    # Get all the requirement item information
    requirement_item_results = RequirementItem.objects.filter(
        is_deleted=False,
        requirement_id=results.requirement_id,
    )

    status_list = ListOfRequirementStatus.objects.filter(
        is_deleted=False,
    )

    status_item_list = ListOfRequirementItemStatus.objects.filter(
        is_deleted=False,
    )

    type_list = ListOfRequirementType.objects.filter(
        is_deleted=False,
    )

    type_item_list = ListOfRequirementItemType.objects.filter(
        is_deleted=False,
    )

    organisation_results = getattr(
        results,
        "organisation"
    )

    # Serialise
    organisation_results = serializers.serialize("json", [organisation_results])
    results = serializers.serialize("json", [results])
    requirement_item_results = serializers.serialize("json", requirement_item_results)
    status_list = serializers.serialize("json", status_list)
    status_item_list = serializers.serialize("json", status_item_list)
    type_list = serializers.serialize("json", type_list)
    type_item_list = serializers.serialize("json", type_item_list)

    return {
        "results": results,
        "requirement_item_results": requirement_item_results,
        "organisation_results": organisation_results,
        "status_list": status_list,
        "status_item_list": status_item_list,
        "type_list": type_list,
        "type_item_list": type_item_list,
    }


# Internal function
def get_public_context_task(results):
    # Get the status data
    status_options = ListOfTaskStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("task_status_id"),
        label=F("task_status"),
    ).values(
        "value",
        "label",
        "task_higher_order_status",
    ).order_by(
        "task_status_order",
    )

    organisation_results = getattr(
        results,
        "organisation"
    )

    # Serialise in the if statement - as None can not be serialized
    organisation_results = serializers.serialize("json", [organisation_results])
    results = serializers.serialize("json", [results])

    return {
        "organisation_results": organisation_results,
        "results": results,
        "status_options": json.dumps(list(status_options), cls=DjangoJSONEncoder),
    }



# Internal function
def get_public_link_results(destination, location_id):
    public_link_results = PublicLink.objects.filter(
        is_deleted=False,
    )

    public_link_results = get_object_from_destination(
        public_link_results, destination, location_id
    )

    # Shape the data
    public_link_results = public_link_results.values(
        "public_link_id",
        "public_link_is_active",
    )

    # Send back json data
    return json.dumps(list(public_link_results), cls=DjangoJSONEncoder)


@login_required(login_url="login", redirect_field_name="")
@check_destination()
def get_public_links(request, destination, location_id):
    # Return the data we have
    public_link_results = get_public_link_results(destination, location_id)

    return HttpResponse(
        public_link_results,
        content_type="application/json"
    )


@check_public_destination()
def public_link(request, destination, location_id, public_link_id, *args, **kwargs):
    # Check to make sure object exists
    public_link_results = PublicLink.objects.filter(
        is_deleted=False,
        public_link_is_active=True,
        public_link_id=public_link_id,
    )

    # Double check everything matches
    public_link_results = get_object_from_destination(
        public_link_results,
        destination,
        location_id,
    )

    # If there are no matching public links - redirect to the login page
    if len(public_link_results) == 0:
        return redirect('login')

    # Get the template
    t = loader.get_template(F"NearBeach/public/public_{destination}_information.html")

    # Get the first results dependent on the destination.
    results = getattr(
        public_link_results.first(),
        destination
    )

    # Depending on the destination, depends on how we setup the context
    if destination == "kanban_card":
        c = get_public_context_kanban_card(results)
    elif destination == "kanban_board":
        c = get_public_context_kanban_board(results)
    elif destination == "requirement":
        c = get_public_context_requirement(results)
    elif destination == "project":
        c = get_public_context_project(results)
    elif destination == "task":
        c = get_public_context_task(results)
    else:
        c = get_public_context(results)

    # Add tinymce flag
    c["need_tinymce"] = True
    c["theme"] = 'light'

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
def update_public_link(request):
    form = PublicLinkUpdateForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the data
    uuid = str(form.cleaned_data["public_link_id"])

    PublicLink.objects.filter(
        public_link_id=uuid,
    ).update(
        public_link_is_active=form.cleaned_data["public_link_is_active"]
    )

    return HttpResponse()
