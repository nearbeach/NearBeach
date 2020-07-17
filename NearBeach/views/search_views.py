from NearBeach.models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound

# Import Forms
from NearBeach.forms import *


@login_required(login_url='login',redirect_field_name="")
def search_organisation_data(request):
    print("GETTING HERE!")
    # Check to make sure it is post
    if not request.method=="POST":
        #Give the user a 404
        return HttpResponseBadRequest("Sorry - Post only")

    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    organisation_results = organisation.objects.filter(is_deleted="FALSE")

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        organisation_results.filter(organisation_name__icontains=split_row)

    # Only have 25 results and order by alphabetical order
    organisation_results.order_by('organisation_name')[:25]

    # Send back json data
    json_results = serializers.serialize('json', organisation_results)

    return HttpResponse(json_results, content_type='application/json')


