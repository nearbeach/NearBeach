from NearBeach.models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound

# Import Forms
from NearBeach.forms import *

def apply_search_term(database_object,search_against,search_term):
    """
    The following will get a database object and search term. It will split the search term into
    an array which will be used to search the database object. The smaller database object is
    sent back.

    Method
    ~~~~~~
    1. Split the search term up
    2. Loop through each search term
    3. Apply it to the database object
    :param database_object:
    :param search_against:
    :param search_term:
    :return:
    """
    for split_row in search_term.split(' '):
        database_object.filter(search_against=split_row)

    return database_object



@login_required(login_url='login',redirect_field_name="")
def search_organisation_data(request):
    print("GETTING HERE!")
    # Check to make sure it is post
    if not request.method=="POST":
        #Give the user a 404
        return HttpResponseNotFound

    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("Search form did not work")

    # Apply the search term to the organisation results
    organisation_results = apply_search_term(
        organisation.objects.filter(is_deleted="FALSE"),
        'organisation_name__icontains',
        search_form.cleaned_data['search']
    )

    # Send back json data
    json_results = serializers.serialize('json', organisation_results)

    return JsonResponse(json_results)



