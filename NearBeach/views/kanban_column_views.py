from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.views.tools.internal_functions import *
from django.db.models import Max
from NearBeach.decorators.check_user_permissions import check_user_permissions, check_user_kanban_permissions
from NearBeach.forms import NewColumnForm
import json, urllib3


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
@check_user_permissions(min_permission_level=2, object_lookup='kanban_board_id')
def edit_column(request, kanban_column_id, *args, **kwargs):
    """
    """
    return HttpResponse("HELLO WORLD")



@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
@check_user_permissions(min_permission_level=3, object_lookup='kanban_board_id')
def new_column(request, kanban_board_id, *args, **kwargs):
    """
    """
    # Get data from form
    form = NewColumnForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create a new column
    kanban_column_submit = kanban_column(
        kanban_column_name=form.cleaned_data['kanban_column_name'],
        kanban_board_id=kanban_board_id,
        kanban_column_sort_number=form.cleaned_data['kanban_column_sort_number'],
        change_user=request.user,
    )

    # Get the information and return as json results
    kanban_column_results = kanban_column.objects.filter(
        kanban_column_id = kanban_column_submit.kanban_column_id,
    )
     
    return HttpResponse(serializers.serialize('json',[kanban_column_submit]), content_type='application/json')
