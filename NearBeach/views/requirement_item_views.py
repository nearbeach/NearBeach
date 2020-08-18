from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level


import json

def new_requirement_item(request,requirement_id):
    return HttpResponse("Hello World... need to create this page")

def new_requirement_item_save(request,requirement_id):
    return HttpResponse("Hello World... need to create this page")

def requirement_item_information(request,requirement_item_id):
    # TO DO - THIS ACTUAL PROGRAM!
    # Get all status - even deleted ones.
    status_list = list_of_requirement_item_status.objects.all()

    # Send back json data
    json_results = serializers.serialize('json', status_list)

    return HttpResponse(json_results, content_type='application/json')