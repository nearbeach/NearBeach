from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from NearBeach.models import KanbanCard

@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["GET"])
def card_information(request, card_id):
    '''
    Will get the card information, and redirect to the correct kanban board

    If there is no card - return a 404.
    '''
    card_results = get_object_or_404(KanbanCard, kanban_card_id=card_id)

    # Using the kanban board id - we can now go to the kanban board
    return redirect(
        "kanban_information",
        kanban_board_id=card_results.kanban_board_id,
        open_card_on_load=card_id,
    )
