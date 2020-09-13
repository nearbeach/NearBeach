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
from NearBeach.views.requirement_views import get_requirement_items


import json

@login_required(login_url='login',redirect_field_name="")
def get_user_requirement_item_permissions(request,requirement_id):
    """
    Use the requirement_id and find out if the user has access to this requirement
    :param requirement_id:
    :return:
    """
    requirement_groups = object_assignment.objects.filter(
        is_deleted="FALSE",
        #requirement_id=requirement_id
    ).values('group_id')

    if requirement_id > 0:
        # Make sure to filter by requirement groups
        requirement_groups = requirement_groups.filter(
            requirement_id=requirement_id
        )

    return return_user_permission_level(request, requirement_groups, ['requirement','requirement_link'])

def new_requirement_item(request,requirement_id):
    # Check to see if POST
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - needs to be in POST")

    # Check user permissions
    permission_results = get_user_requirement_item_permissions(request, requirement_id)

    # If user has no permissions to create requirements or requirement items, then send them to the appropriate location
    if permission_results['requirement'] <= 2 and permission_results['requirement_item'] <= 2:
        # Users can not create requirement.
        return HttpResponseRedirect(reverse('permission_denied'))

    # Get the data into the form for cleaning
    form = NewRequirementItemForm(request.POST)

    # Check to make sure there are no errors in the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_requirement_item = requirement_item(
        requirement=requirement.objects.get(requirement_id=requirement_id),
        requirement_item_title=form.cleaned_data['requirement_item_title'],
        requirement_item_scope=form.cleaned_data['requirement_item_scope'],
        requirement_item_status=form.cleaned_data['requirement_item_status'],
        requirement_item_type=form.cleaned_data['requirement_item_type'],
        change_user=request.user,
    )
    submit_requirement_item.save()

    # Actuall return all the new requirement_item results to feed upstream
    return get_requirement_items(request,requirement_id)

def requirement_item_information(request,requirement_item_id):
    # TO DO - THIS ACTUAL PROGRAM!
    # Get all status - even deleted ones.
    status_list = list_of_requirement_item_status.objects.all()

    # Send back json data
    json_results = serializers.serialize('json', status_list)

    return HttpResponse(json_results, content_type='application/json')