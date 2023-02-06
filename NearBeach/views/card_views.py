from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from NearBeach.models import KanbanBoard, KanbanCard


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["GET"])
def card_information(request, card_id):
    # Get the card or 404
    card_results = get_object_or_404(KanbanCard, kanban_card_id=card_id)

    # Using the kanban board id - we can now go to the kanban board
    return redirect(
        'kanban_information',
        kanban_board_id=card_results.kanban_board_id,
        open_card_on_load=card_id
    )
