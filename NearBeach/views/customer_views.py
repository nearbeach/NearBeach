from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import check_user_customer_permissions

import json


@login_required(login_url='login',redirect_field_name='')
@check_user_customer_permissions(min_permission_level=1)
def customer_information(request,customer_id, *args, **kwargs):
    """

    :param request:
    :param customer_id:
    :return:
    """
    # Find out if the user is read only - if they are send them to the read only

    # Get customer data
    customer_results = customer.objects.get(customer_id=customer_id)

    print("Customer Organisation id: %s " % customer_results.organisation_id)

    organisation_results = organisation.objects.filter(
        organisation_id=customer_results.organisation_id,
    )

    title_list = list_of_title.objects.filter(
        #is_deleted=False, # NEED TO RECONSTRUCT DATABASE TO GET THIS TO WORK!
    )

    # Get tempalte
    t = loader.get_template('NearBeach/customers/customer_information.html')

    # Context
    c = {
        'customer_results': serializers.serialize('json',[customer_results]),
        'organisation_results': serializers.serialize('json', organisation_results),
        'title_list': serializers.serialize('json',title_list),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
@check_user_customer_permissions(min_permission_level=2)
def customer_information_save(request,customer_id, *args, **kwargs):
    """

    :param request:
    :param customer_id:
    :return:
    """
    # ADD IN USER PERMISSION CHECKS

    # Get form data
    form = CustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the customer instance
    customer_results = customer.objects.get(customer_id=customer_id)

    # Update the fields
    customer_results.customer_title = form.cleaned_data['customer_title']
    customer_results.customer_first_name = form.cleaned_data['customer_first_name']
    customer_results.customer_last_name = form.cleaned_data['customer_last_name']
    customer_results.customer_email = form.cleaned_data['customer_email']
    # customer_results.organisation = form.cleaned_data['organisation'] # Does not need updating!

    # Save
    customer_results.save()

    # Return back a sucessful statement
    return HttpResponse("Success")


@login_required(login_url='login',redirect_field_name="")
@check_user_customer_permissions(min_permission_level=3)
def new_customer(request, *args, **kwargs):
    """

    :param request:
    :return:
    """
    # Get user permission

    # Get data
    title_list = list_of_title.objects.filter(
        is_deleted=False,
    )

    # Get templates
    t = loader.get_template('NearBeach/customers/new_customers.html')

    # Get Context
    c = {
        'title_list': serializers.serialize('json',title_list),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def new_customer_save(request, *args, **kwargs):
    """

    :param reqeust:
    :return:
    """

    # CHECK USER PERMISSIONS -- NEED TO ADD THIS IN!

    # Get Form data
    form = NewCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    customer_submit = customer(
        change_user=request.user,
        customer_title=form.cleaned_data['customer_title'],
        customer_first_name=form.cleaned_data['customer_first_name'],
        customer_last_name=form.cleaned_data['customer_last_name'],
        customer_email=form.cleaned_data['customer_email'],
    )

    # If the organisation is not null in the form - set the data
    if form.cleaned_data['organisation']:
        customer_submit.organisation = form.cleaned_data['organisation']

    # Save the data
    customer_submit.save()

    # Send back the URL to the new customer
    return HttpResponse(reverse('customer_information', args={customer_submit.customer_id}))
