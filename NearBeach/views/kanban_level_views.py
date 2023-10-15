from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import check_user_permissions
from NearBeach.forms import NewLevelForm, KanbanLevel, DeleteLevelForm, ResortLevelForm
from NearBeach.views.tools.internal_functions import KanbanCard


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def edit_level(request, kanban_level_id, *args, **kwargs):
    """
    Edits/Updates a kanban level
    :param: kanban_level_id: The level id we are editing
    """
    form = NewLevelForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the instance
    kanban_level_results = KanbanLevel.objects.get(
        kanban_level_id=kanban_level_id,
    )

    # Update the data
    kanban_level_results.kanban_level_name = form.cleaned_data["kanban_level_name"]
    kanban_level_results.kanban_level_sort_number = form.cleaned_data[
        "kanban_level_sort_number"
    ]

    # Save the data
    kanban_level_results.save()

    # Return the data
    return HttpResponse(
        serializers.serialize("json", [kanban_level_results]),
        content_type="application/json",
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_user_permissions(min_permission_level=4, object_lookup="kanban_board_id")
def delete_level(request, kanban_board_id, *args, **kwargs):
    """
    Deletes a level
    :param: kanban_board_id: The board we are focusing on
    """
    form = DeleteLevelForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    destination_item_id = form.cleaned_data["destination_item_id"]

    # Update the variables
    if destination_item_id is None:
        # There is no destination for the cards - flag deleted
        KanbanCard.objects.filter(
            is_deleted=False,
            kanban_level_id=form.cleaned_data["delete_item_id"],
            kanban_board_id=kanban_board_id,
        ).update(is_deleted=True)
    else:
        # There is a destination - update to that destination
        KanbanCard.objects.filter(
            is_deleted=False,
            kanban_level_id=form.cleaned_data["delete_item_id"],
            kanban_board_id=kanban_board_id,
        ).update(kanban_level_id=form.cleaned_data["destination_item_id"])

    # Soft delete the old column
    deleted_level = KanbanLevel.objects.get(
        kanban_level_id=form.cleaned_data["delete_item_id"].kanban_level_id,
        kanban_board_id=kanban_board_id,
    )
    deleted_level.is_deleted = True
    deleted_level.save()

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_user_permissions(min_permission_level=3, object_lookup="kanban_board_id")
def new_level(request, kanban_board_id, *args, **kwargs):
    """
    Creates a new level for a kanban board
    :param: kanban_board_id: is the baord we are focusing on
    """
    form = NewLevelForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create a new level
    kanban_level_submit = KanbanLevel(
        kanban_level_name=form.cleaned_data["kanban_level_name"],
        kanban_board_id=kanban_board_id,
        kanban_level_sort_number=form.cleaned_data["kanban_level_sort_number"],
        change_user=request.user,
    )
    kanban_level_submit.save()

    # Get the information and return as json results
    _ = KanbanLevel.objects.filter(
        kanban_level_id=kanban_level_submit.kanban_level_id,
    )

    return HttpResponse(
        serializers.serialize("json", [kanban_level_submit]),
        content_type="application/json",
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
@check_user_permissions(min_permission_level=2, object_lookup="kanban_board_id")
def resort_level(request, kanban_board_id, *args, **kwargs):
    """
    Resorts the levels when updated
    :param: kanban_board_id: Focusing on this board
    """
    form = ResortLevelForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the data
    items = request.POST.getlist("item")

    # Look through the item list and re-index the order
    for index, item in enumerate(items, start=0):
        kanban_level_update = KanbanLevel.objects.get(
            kanban_level_id=item,
            kanban_board_id=kanban_board_id
        )
        kanban_level_update.kanban_level_sort_number = index
        kanban_level_update.save()

    return HttpResponse("")
