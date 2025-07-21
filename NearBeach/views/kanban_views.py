import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.shortcuts import get_object_or_404

from NearBeach.models import (
    KanbanColumn,
    KanbanLevel,
    ObjectAssignment,
    Group,
    TagAssignment,
    UserSetting,
)
from NearBeach.views.search.kanban_link_list import KanbanLinkList
from NearBeach.views.theme_views import get_theme
from NearBeach.views.tools.internal_functions import (
    get_all_groups,
    get_user_group_permission,
    KanbanCard,
    KanbanBoard,
    Project,
    Requirement,
    RequirementItem,
    Task,
)
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions
from NearBeach.forms import (
    AddKanbanLinkForm,
    FixCardOrderingForm,
    KanbanCardArchiveForm,
    CheckKanbanBoardName,
    MoveKanbanCardForm,
    NewKanbanCardForm,
    NewKanbanForm,
    KanbanCardForm,
    SearchObjectsForm,
)
from NearBeach import event_hooks
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Max
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache

LOOKUP_FUNCS = {
    "project": {
        "object": Project.objects,
        "title": "project_name",
        "parent": "project",
    },
    "task": {
        "object": Task.objects,
        "title": "task_short_description",
        "parent": "task",
    },
    "requirement": {
        "object": Requirement.objects,
        "title": "requirement_title",
        "parent": "requirement",
    },
    "requirement_item": {
        "object": RequirementItem.objects,
        "title": "requirement_item_title",
        "parent": "requirement",
    },
}

event_hooks.register_event_type("kanban_card.create", KanbanCard)
event_hooks.register_event_type("kanban_card.changed_column", KanbanCard)

@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=2, object_lookup="kanban_board")
def add_kanban_link(request, kanban_board_id, object_lookup, *args, **kwargs):
    """
    Adds a link to an object to a kanban board
    :param request:
    :param kanban_board_id: The board we are focusing on
    :param object_lookup: The object we are linking 
    :return:
    """
    form = AddKanbanLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the newest card number id
    kanban_card_sort_number = get_max_sort_id(kanban_board_id, form)

    # Submit the kanban board link
    kanban_card_submit = KanbanCard(
        change_user=request.user,
        kanban_board_id=kanban_board_id,
        kanban_column=form.cleaned_data["kanban_column"],
        kanban_level=form.cleaned_data["kanban_level"],
        kanban_card_sort_number=kanban_card_sort_number + 1,
    )

    # Check the data
    data = form.cleaned_data[object_lookup]
    if object_lookup == "project":
        kanban_card_submit.project = data
        kanban_card_submit.kanban_card_description = data.project_description
        kanban_card_submit.kanban_card_priority = data.project_priority
    elif object_lookup == "task":
        kanban_card_submit.task = data
        kanban_card_submit.kanban_card_description = data.task_long_description
        kanban_card_submit.kanban_card_priority = data.task_priority
    elif object_lookup == "requirement":
        kanban_card_submit.requirement = data
        kanban_card_submit.kanban_card_description = data.requirement_scope

    kanban_card_submit.kanban_card_text = form.cleaned_data[object_lookup]

    # Save the data
    kanban_card_submit.save()
    event_hooks.emit("kanban_card.create", kanban_card_submit)

    # Send back the kanban card data
    kanban_card_results = KanbanCard.objects.filter(
        kanban_card_id=kanban_card_submit.kanban_card_id
    ).values(
       "kanban_card_description",
       "kanban_card_id",
       "kanban_card_priority",
       "kanban_card_sort_number",
       "kanban_card_text",
       "kanban_column",
       "kanban_level",
       "project",
       "requirement",
       "task",
    )
    kanban_card_results = json.dumps(list(kanban_card_results), cls=DjangoJSONEncoder)

    return JsonResponse(json.loads(kanban_card_results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=2, object_lookup="kanban_board")
def archive_kanban_cards(request, *args, **kwargs):
    """Archive the kanban cards."""
    form = KanbanCardArchiveForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get all cards from POST
    card_list = request.POST.getlist("kanban_card_id")

    # Update all cards
    KanbanCard.objects.filter(kanban_card_id__in=card_list,).update(
        is_archived=True,
    )

    # Return success
    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_board")
def check_kanban_board_name(request, *args, **kwargs):
    """
    The following will get a list of all kanban boards with the same name. The idea is that each kanban board should
    have a unique name.
    :param request:
    :return:
    """
    form = CheckKanbanBoardName(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    kanban_board_results = KanbanBoard.objects.filter(
        is_deleted=False,
        kanban_board_name=form.cleaned_data["kanban_board_name"],
    )

    # Send back data
    return HttpResponse(
        serializers.serialize("json", kanban_board_results),
        content_type="application/json",
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=1, object_lookup="kanban_board")
def fix_card_ordering(request, *args, **kwargs):
    form = FixCardOrderingForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the kanban cards data
    kanban_cards = form.cleaned_data['kanban_cards']

    # Loop through each card - and update it's order
    for index, single_card in enumerate(kanban_cards):
        single_card.kanban_card_sort_number = index
        single_card.save()

    return HttpResponse("")


# Internal function
def get_context(kanban_board_id):
    # Get the kanban data
    kanban_board_results = KanbanBoard.objects.filter(is_deleted=False)
    kanban_board_results = get_object_or_404(kanban_board_results, kanban_board_id=kanban_board_id)

    column_results = KanbanColumn.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    ).order_by(
        "kanban_column_sort_number",
    )

    level_results = KanbanLevel.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    ).order_by(
        "kanban_level_sort_number",
    )

    # Context
    c = {
        "kanban_board_results": serializers.serialize("json", [kanban_board_results]),
        "column_results": serializers.serialize("json", column_results),
        "kanban_board_id": kanban_board_id,
        "level_results": serializers.serialize("json", level_results),
        "nearbeach_title": f"Kanban Information {kanban_board_id}",
        "kanban_board_status": kanban_board_results.kanban_board_status,
    }

    return c


# Internal function
def get_max_sort_id(kanban_board_id, form):
    """Get the newest card number id"""
    kanban_card_sort_number = KanbanCard.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
        kanban_column=form.cleaned_data["kanban_column"],
        kanban_level=form.cleaned_data["kanban_level"],
    ).aggregate(Max("kanban_card_sort_number"))

    # If the card is new in that particular column & row - then we need to implement a sort number of 0
    if kanban_card_sort_number["kanban_card_sort_number__max"] is None:
        kanban_card_sort_number["kanban_card_sort_number__max"] = 0

    return kanban_card_sort_number["kanban_card_sort_number__max"]


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_board")
def kanban_close_board(request, kanban_board_id, *args, **kwargs):
    """Close the kanban board"""
    kanban_update = KanbanBoard.objects.get(kanban_board_id=kanban_board_id)
    kanban_update.kanban_board_status = "Closed"
    kanban_update.save()

    # Return Success
    return HttpResponse("")


@never_cache
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_board")
def kanban_edit_board(request, kanban_board_id, *args, **kwargs):
    """Edit the permissions of the kanban board"""
    user_level = kwargs["user_level"]

    # Get group results
    group_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        group_id__isnull=False,
        kanban_board_id=kanban_board_id,
    )

    # Get context
    c = get_context(kanban_board_id)
    c["theme"] = get_theme(request)
    c["need_tinymce"] = False
    c["user_level"] = user_level
    c["group_results"] = serializers.serialize("json", group_results)

    # Convert the closed status into JavaScript boolean
    if c["kanban_board_status"] == "Closed":
        c["kanban_board_is_closed"] = "true"
    else:
        c["kanban_board_is_closed"] = "false"

    # Get the template
    t = loader.get_template("NearBeach/kanban/kanban_edit_board.html")

    # Get the context
    return HttpResponse(t.render(c, request))


@never_cache
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="kanban_board")
def kanban_information(request, kanban_board_id, *args, open_card_on_load=0, **kwargs,):
    """
    Renders out the kanban board information
    :param request:
    :param kanban_board_id: The board id we wish to render out
    :param open_card_on_load: Will open a card if value is placed in here. Zero is default
    :return:
    """
    user_level = kwargs["user_level"]

    # Get kanban card results
    kanban_card_results = KanbanCard.objects.filter(
        is_archived=False,
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    ).values(
        "kanban_card_id",
        "kanban_card_description",
        "kanban_card_priority",
        "kanban_card_sort_number",
        "kanban_card_text",
        "kanban_column",
        "kanban_level",
        "project",
        "requirement",
        "task",
        "date_created",
        "date_modified",
    ).order_by(
        "kanban_card_sort_number"
    )

    tag_results = TagAssignment.objects.filter(
        is_deleted=False,
        object_enum="kanban_card",
        object_id__in=kanban_card_results.values("kanban_card_id"),
    ).annotate(
        kanban_card_id=F("object_id"),
        tag_name=F("tag__tag_name"),
        tag_colour=F("tag__tag_colour"),
        tag_text_colour=F("tag__tag_text_colour"),
    ).values(
        "kanban_card_id",
        "tag_assignment_id",
        "tag_id",
        "tag_name",
        "tag_colour",
        "tag_text_colour",
    )

    kanban_card_results = json.dumps(list(kanban_card_results), cls=DjangoJSONEncoder)
    tag_results = json.dumps(list(tag_results), cls=DjangoJSONEncoder)

    # Get kanban user settings
    kanban_settings = UserSetting.objects.filter(
        username=request.user,
        setting_type="KANBAN_BOARD"
    ).values(
        "setting_data"
    ).first()
    if kanban_settings is None:
        kanban_settings = {}

    # Get context
    c = get_context(kanban_board_id)
    c["theme"] = get_theme(request)
    c["need_tinymce"] = True
    c["user_level"] = user_level
    c["kanban_card_results"] = json.loads(kanban_card_results)
    c["kanban_settings"] = json.dumps(kanban_settings)
    c["open_card_on_load"] = open_card_on_load
    c["tag_results"] = json.loads(tag_results)

    # Get the template
    t = loader.get_template("NearBeach/kanban/kanban_information.html")

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=1, object_lookup="kanban_board")
def kanban_link_list(request, kanban_board_id, *args, **kwargs):
    """
    Obtains the data for the kanban links
    :param request:
    :param kanban_board_id:
    :return:
    """
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    results = KanbanLinkList(form, request)

    # Return the json data
    return JsonResponse(results.results)


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_board")
def kanban_reopen_board(request, kanban_board_id, *args, **kwargs):
    """Reopen the kanban board"""
    kanban_update = KanbanBoard.objects.get(kanban_board_id=kanban_board_id)
    kanban_update.kanban_board_status = "Open"
    kanban_update.save()

    # Return Success
    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=2, object_lookup="kanban_card")
def move_kanban_card(request, kanban_card_id, *args, **kwargs):
    """
    Updates a kanban kard when it moves
    :param request:
    :param kanban_card_id: The card we are focusing on
    :return:
    """
    kanban_card_update = KanbanCard.objects.get(kanban_card_id=kanban_card_id)

    # Get the form data
    form = MoveKanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    dest_column = form.cleaned_data["new_card_column"]
    dest_level = form.cleaned_data["new_card_level"]

    # Used later to figure out if it should emit an event
    moved_column = kanban_card_update.kanban_column != dest_column

    # Update the card data
    kanban_card_update.kanban_column = dest_column
    kanban_card_update.kanban_level = dest_level

    """
    Update the sort order
    ~~~~~~~~~~~~~~~~~~~~~

    The front end will send the following data;
    - new_destination
    - old_destination

    This is a ()set of kanban cards that are in the correct order. We'll loop through these cards and update them.

    The old destination ()set is optional.
    """

    # Update new location's cards
    for index, card in enumerate(form.cleaned_data['new_destination']):
        if card.kanban_card_id == kanban_card_update.kanban_card_id:
            # Update ordering for the updated card
            kanban_card_update.kanban_card_sort_number = index
            kanban_card_update.save()
        else:
            # Reorder untouched card
            card.kanban_card_sort_number = index
            card.save()

    # Update old location's cards
    for index, card in enumerate(form.cleaned_data['old_destination']):
        card.kanban_card_sort_number = index
        card.save()

    if moved_column:
        event_hooks.emit("kanban_card.changed_column", kanban_card_update)

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_card")
def new_kanban(request, *args, **kwargs):
    """
    Controller for the "/new_kanban" route

    :param request: Django variable
    :return: Http Request
    """
    # Get tempalte
    t = loader.get_template("NearBeach/kanban/new_kanban.html")

    # Context
    c = {
        "group_results": get_all_groups(),
        "need_tinymce": False,
        "nearbeach_title": "New Kanban",
        "user_group_permissions": get_user_group_permission(request.user, ["kanban_board"]),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=2, object_lookup="kanban_board")
def new_kanban_card(request, kanban_board_id, *args, **kwargs):
    """Add a new kanban card"""
    kanban_instance = KanbanBoard.objects.get(kanban_board_id=kanban_board_id)

    # Get the form data
    form = NewKanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the newest card number id
    kanban_card_sort_number = get_max_sort_id(kanban_board_id, form)

    # Save the data
    submit_kanban_card = KanbanCard(
        change_user=request.user,
        kanban_board=kanban_instance,
        kanban_card_text=form.cleaned_data["kanban_card_text"],
        kanban_card_description=form.cleaned_data["kanban_card_description"],
        kanban_column=form.cleaned_data["kanban_column"],
        kanban_level=form.cleaned_data["kanban_level"],
        kanban_card_sort_number=kanban_card_sort_number + 1,
        kanban_card_priority=form.cleaned_data["kanban_card_priority"],
    )
    submit_kanban_card.save()

    # Send back the kanban card data
    kanban_card_results = KanbanCard.objects.filter(
        kanban_card_id=submit_kanban_card.kanban_card_id
    ).values(
        "kanban_card_description",
        "kanban_card_id",
        "kanban_card_priority",
        "kanban_card_sort_number",
        "kanban_card_text",
        "kanban_column",
        "kanban_level",
        "project",
        "requirement",
        "task",
        "date_created",
        "date_modified",
    )
    kanban_card_results = json.dumps(list(kanban_card_results), cls=DjangoJSONEncoder)

    return JsonResponse(json.loads(kanban_card_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_card")
def new_kanban_save(request, *args, **kwargs):
    """
    Saves the new kanban board
    :param request:
    :return:
    """
    # Check the user form
    form = NewKanbanForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the kanban board
    submit_kanban_board = KanbanBoard(
        change_user=request.user,
        creation_user=request.user,
        kanban_board_name=form.cleaned_data["kanban_board_name"],
    )
    submit_kanban_board.save()

    # Get both lists
    column_title_list = request.POST.getlist("column_title")
    column_property_list = request.POST.getlist("column_property")
    level_title_list = request.POST.getlist("level_title")

    # Loop through the column title list to save the titles
    for index, column_title in enumerate(column_title_list):
        submit_column_title = KanbanColumn(
            change_user=request.user,
            kanban_column_name=column_title,
            kanban_column_property=column_property_list[index],
            kanban_board=submit_kanban_board,
            kanban_column_sort_number=index,
        )
        submit_column_title.save()

    # Loop throuhg the level title list to save the titles
    for index, level_title in enumerate(level_title_list):
        submit_level_title = KanbanLevel(
            change_user=request.user,
            kanban_level_name=level_title,
            kanban_board=submit_kanban_board,
            kanban_level_sort_number=index,
        )
        submit_level_title.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = Group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = ObjectAssignment(
            group_id=group_instance,
            kanban_board=submit_kanban_board,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back project_information URL
    return HttpResponse(
        reverse("kanban_information", args=[submit_kanban_board.kanban_board_id])
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=2, object_lookup="kanban_card")
def update_card(request, *args, **kwargs):
    """
    The following function will update the card information
    from which is sent through the form in POST
    """
    form = KanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    kanban_card_update = form.cleaned_data["kanban_card_id"]
    kanban_card_update.kanban_card_text = form.cleaned_data["kanban_card_text"]
    kanban_card_update.kanban_card_description = form.cleaned_data[
        "kanban_card_description"
    ]
    kanban_card_update.kanban_card_priority = form.cleaned_data["kanban_card_priority"]
    kanban_card_update.kanban_column = form.cleaned_data["kanban_column"]
    kanban_card_update.kanban_level = form.cleaned_data["kanban_level"]

    # If we move the card's destination, we want to update the sort order in both the old and new destination
    new_destination = form.cleaned_data['new_destination']
    old_destination = form.cleaned_data['old_destination']

    for index, card in enumerate(new_destination):
        if card.kanban_card_id == kanban_card_update.kanban_card_id:
            kanban_card_update.kanban_card_sort_number = index
        else:
            card.kanban_card_sort_number = index
            card.save()

    for index, card in enumerate(old_destination):
        card.kanban_card_sort_number = index
        card.save()

    # Save late, as multiple saves causes an override issue.
    kanban_card_update.save()

    return HttpResponse("")


# Internal Function
def update_sort_number(resort_array, delta):
    """
    The following function will loop through the resort array and apply the delta (which should be either a 1 or -1)
    :param resort_array:
    :param delta:
    :return:
    """
    for row in resort_array:
        row.kanban_card_sort_number = row.kanban_card_sort_number + delta
        row.save()
