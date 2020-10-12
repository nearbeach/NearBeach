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
from NearBeach.user_permissions import return_user_permission_level
from django.views.decorators.http import require_http_methods


import json


@login_required(login_url='login',redirect_field_name="")
def new_organisation(request):
    """

    :param request:
    :return:
    """
    # Get user permission

    # Get templates
    t = loader.get_template('NearBeach/organisations/new_organisations.html')

    # Get Context
    c = {}

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
def new_organisation_save(request):
    """

    :param request:
    :return:
    """
    permission_results = return_user_permission_level(request, None, 'organisation')

    if permission_results['organisation'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))

    # Get the data
    form = OrganisationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    organisation_submit = organisation(
        change_user=request.user,
        organisation_name=form.cleaned_data['organisation_name'],
        organisation_email=form.cleaned_data['organisation_email'],
        organisation_website=form.cleaned_data['organisation_website'],
    )
    organisation_submit.save()

    return HttpResponse(reverse('organisation_information',args={organisation_submit.organisation_id}))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def organisation_duplicates(request):
    """

    :param request:
    :return:
    """

    # ADD IN USER PERMISSION CHECKS

    # Extract data from POST
    form = OrganisationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Check to see if there are any matches
    organisation_results = organisation.objects.filter(
        Q(
            is_deleted=False,
        ) & Q(
            Q(organisation_name__contains=form.cleaned_data['organisation_name']) |
            Q(organisation_website__contains=form.cleaned_data['organisation_website']) |
            Q(organisation_email__contains=form.cleaned_data['organisation_email'])
        )
    )

    return HttpResponse(serializers.serialize('json',organisation_results),content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def organisation_information(request,organisation_id):
    """

    :param request:
    :param organisation_id:
    :return:
    """
    organisation_results = organisation.objects.get(organisation_id=organisation_id)

    customer_results = customer.objects.filter(
        is_deleted=False,
        organisation_id=organisation_id,
    )

    title_list = list_of_title.objects.filter(
        is_deleted=False,
    )

    t = loader.get_template('NearBeach/organisations/organisation_information.html')

    c = {
        'customer_results': serializers.serialize('json',customer_results),
        'organisation_id': organisation_id,
        'organisation_results': serializers.serialize('json',[organisation_results]),
        'title_list': serializers.serialize('json',title_list),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def organisation_information_save(request,organisation_id):
    """

    :param request:
    :param organisation_id:
    :return:
    """

    # ADD IN PERMISSION CHECKING

    # Get the form data
    form = OrganisationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the instance
    organisation_instance = organisation.objects.get(organisation_id=organisation_id)
    organisation_instance.organisation_name = form.cleaned_data['organisation_name']
    organisation_instance.organisation_email = form.cleaned_data['organisation_email']
    organisation_instance.organisation_website = form.cleaned_data['organisation_website']
    organisation_instance.save()

    return HttpResponse('')


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def organisation_update_profile(request,organisation_id):
    """

    :param request:
    :param organisation_id:
    :return:
    """
    return HttpResponse('')