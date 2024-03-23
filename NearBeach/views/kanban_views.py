import json

from django.shortcuts import get_object_or_404

from NearBeach.models import (
    KanbanColumn,
    KanbanLevel,
    ObjectAssignment,
    Group,
    UserGroup,
    UserSetting,
)
from NearBeach.views.theme_views import get_theme
from NearBeach.views.tools.internal_functions import (
    KanbanCard,
    KanbanBoard,
    Project,
    Requirement,
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
)
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache


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
    if object_lookup == "project":
        kanban_card_submit.project = form.cleaned_data[object_lookup]
    elif object_lookup == "task":
        kanban_card_submit.task = form.cleaned_data[object_lookup]
    elif object_lookup == "requirement":
        kanban_card_submit.requirement = form.cleaned_data[object_lookup]

    kanban_card_submit.kanban_card_text = form.cleaned_data[object_lookup]

    # Save the data
    kanban_card_submit.save()

    # Send back the data we just created
    kanban_card_results = KanbanCard.objects.get(
        kanban_card_id=kanban_card_submit.kanban_card_id
    )

    return HttpResponse(
        serializers.serialize("json", [kanban_card_results]),
        content_type="application/json",
    )


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
    ).order_by("kanban_card_sort_number")

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
    c["kanban_card_results"] = serializers.serialize("json", kanban_card_results)
    c["kanban_settings"] = json.dumps(kanban_settings)
    c["open_card_on_load"] = open_card_on_load

    # Get the template
    t = loader.get_template("NearBeach/kanban/kanban_information.html")

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_specific_object_permissions(min_permission_level=1, object_lookup="kanban_board")
def kanban_link_list(request, kanban_board_id, object_lookup, *args, **kwargs):
    """
    Obtains the data for the kanban links
    :param request:
    :param kanban_board_id:
    :return:
    """
    existing_objects = KanbanCard.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    )

    # Get the results we require
    if object_lookup == "Project":
        object_results = Project.objects.filter(is_deleted=False,).exclude(
            project_id__in=existing_objects.exclude(project_id__isnull=True).values(
                "project_id"
            )
        )
    elif object_lookup == "Requirement":
        object_results = Requirement.objects.filter(is_deleted=False,).exclude(
            requirement_id__in=existing_objects.exclude(
                requirement_id__isnull=True
            ).values("requirement_id")
        )
    elif object_lookup == "Task":
        object_results = Task.objects.filter(is_deleted=False,).exclude(
            task_id__in=existing_objects.exclude(
                task_id__isnull=True,
            ).values("task_id")
        )
    else:
        return HttpResponseBadRequest(
            "Sorry - there was an issue with your object lookup"
        )

    return HttpResponse(
        serializers.serialize("json", object_results), content_type="application/json"
    )


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

    # Update the card data
    kanban_card_update.kanban_column = form.cleaned_data["new_card_column"]
    kanban_card_update.kanban_level = form.cleaned_data["new_card_level"]
    # kanban_card_update.save()

    """
    Update the sort order
    ~~~~~~~~~~~~~~~~~~~~~
   
    The front end will send the following data;
    - new_destination
    - old_destination
    
    This is a ()set of kanban cards that are in the correct order. We'll loop through these cards and update them.
    
    The old destination ()set is optional.
    """
    new_destination = form.cleaned_data['new_destination']
    old_destination = form.cleaned_data['old_destination']

    for index, card in enumerate(new_destination):
        if card.kanban_card_id == kanban_card_update.kanban_card_id:
            kanban_card_update.kanban_card_sort_number = index
            kanban_card_update.save()
        else:
            card.kanban_card_sort_number = index
            card.save()

    for index, card in enumerate(old_destination):
        card.kanban_card_sort_number = index
        card.save()

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="kanban_card")
def new_kanban(request, *args, **kwargs):
    """
    Renders out the new kanban page
    :param request:
    :return:
    """
    # Check user permissions

    # Get data
    group_results = Group.objects.filter(
        is_deleted=False,
    )

    # Get list of user groups
    user_group_results = (
        UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        )
        .values(
            "group_id",
            "group__group_name",
        )
        .distinct()
    )

    # Get tempalte
    t = loader.get_template("NearBeach/kanban/new_kanban.html")

    # Context
    c = {
        "group_results": serializers.serialize("json", group_results),
        "need_tinymce": False,
        "nearbeach_title": "New Kanban",
        "user_group_results": json.dumps(
            list(user_group_results), cls=DjangoJSONEncoder
        ),
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
    kanban_card_results = KanbanCard.objects.get(
        kanban_card_id=submit_kanban_card.kanban_card_id
    )
    return HttpResponse(
        serializers.serialize("json", [kanban_card_results]),
        content_type="application/json",
    )


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
        reverse("kanban_information", args={submit_kanban_board.kanban_board_id})
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
    kanban_card_update.save()


    # If we move the card's destination, we want to update the sort order in both the old and new destination
    new_destination = form.cleaned_data['new_destination']
    old_destination = form.cleaned_data['old_destination']

    for index, card in enumerate(new_destination):
        if card.kanban_card_id == kanban_card_update.kanban_card_id:
            kanban_card_update.kanban_card_sort_number = index
            kanban_card_update.save()
        else:
            card.kanban_card_sort_number = index
            card.save()

    for index, card in enumerate(old_destination):
        card.kanban_card_sort_number = index
        card.save()

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
