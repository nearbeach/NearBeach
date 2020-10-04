from NearBeach.models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# Import Forms
from NearBeach.forms import *


@login_required(login_url='login',redirect_field_name="")
def search_customer(request):
    """

    :param request:
    :return:
    """
    t = loader.get_template('NearBeach/search/search_customers.html')

    # Get the first 50 customers
    customer_results = customer.objects.filter(
        is_deleted=False,
    ).order_by('customer_last_name','customer_first_name')[:50]

    c = {
        'customer_results': serializers.serialize('json',customer_results)
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_customer_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    customer_results = customer.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the organisation results SQL
        customer_results = customer_results.filter(
            Q(customer_first_name__icontains=split_row) |
            Q(customer_last_name__icontains=split_row) |
            Q(organisation__organisation_name__icontains=split_row) # Might not work for freelancers
        )

    # Only have 50 results and order by alphabetical order
    customer_results.order_by('customer_last_name','customer_first_name')[:50]

    # Send back json data
    json_results = serializers.serialize('json', customer_results)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def search_organisation(request):
    """

    :param request:
    :return:
    """
    t = loader.get_template('NearBeach/search/search_organisations.html')

    # Get the first 25 organisations
    organisation_results = organisation.objects.filter(
        is_deleted=False,
    ).order_by('organisation_name')[:25]

    c = {
        'organisation_results': serializers.serialize('json',organisation_results),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_organisation_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    organisation_results = organisation.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the organisation results SQL
        organisation_results = organisation_results.filter(
            organisation_name__icontains=split_row
        )

    # Only have 25 results and order by alphabetical order
    organisation_results.order_by('organisation_name')[:25]

    # Send back json data
    json_results = serializers.serialize('json', organisation_results)

    return HttpResponse(json_results, content_type='application/json')


