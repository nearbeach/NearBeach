from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers

from NearBeach.models import *
from NearBeach.forms import NewRequestForChangeForm


@login_required(login_url='login', redirect_field_name="")
def new_request_for_change(request):
    """

    :param request:
    :return:
    """

    # CHECK USER PERMISSIONS

    # Get template
    t = loader.get_template('NearBeach/request_for_change/new_request_for_change.html')

    # Get data
    group_results = group.objects.filter(
        is_deleted=False,
    )

    user_results = User.objects.filter( #This should only be group leaders
        is_active=True,
    )

    # Context
    c = {
        'group_results': serializers.serialize('json', group_results),
        'user_results': serializers.serialize('json', user_results),
    }

    return HttpResponse(t.render(c,request))


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def new_request_for_change_save(request):
    """

    :param request:
    :return:
    """

    # Check the user's permission

    # Get the form data
    form = NewRequestForChangeForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return HttpResponseBadRequest(form.errors)

    # Save the data
    rfc_submit = request_for_change(
        change_user=request.user,
        creation_user=request.user,
        rfc_status=1,
        rfc_title=form.cleaned_data['rfc_title'],
        rfc_summary=form.cleaned_data['rfc_summary'],
        rfc_type=form.cleaned_data['rfc_type'],
        rfc_implementation_start_date=form.cleaned_data['rfc_implementation_start_date'],
        rfc_implementation_end_date=form.cleaned_data['rfc_implementation_end_date'],
        rfc_implementation_release_date=form.cleaned_data['rfc_implementation_release_date'],
        rfc_version_number=form.cleaned_data['rfc_version_number'],
        rfc_lead=form.cleaned_data['rfc_lead'],
        rfc_priority=form.cleaned_data['rfc_priority'],
        rfc_risk=form.cleaned_data['rfc_risk'],
        rfc_impact=form.cleaned_data['rfc_impact'],
        rfc_risk_and_impact_analysis=form.cleaned_data['rfc_risk_and_impact_analysis'],
        rfc_implementation_plan=form.cleaned_data['rfc_implementation_plan'],
        rfc_backout_plan=form.cleaned_data['rfc_backout_plan'],
        rfc_test_plan=form.cleaned_data['rfc_test_plan'],
    )
    rfc_submit.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            request_for_change=rfc_submit,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(reverse('rfc_information', args={rfc_submit.rfc_id}))


def rfc_information(request,rfc_id):
    """

    :param request:
    :param rfc_id:
    :return:
    """
    return HttpResponse("Hello World")