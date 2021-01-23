from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers

from NearBeach.models import *
from NearBeach.forms import NewRequestForChangeForm, RfcModuleForm, RfcInformationSaveForm


# Internal function
def get_rfc_context(rfc_id):
    """
    Using the rfc ID, it will extract the required context for the rfc_information and rfc_readonly
    :param rfc_id:
    :return:
    """
    # Get data
    rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
    rfc_change_lead = User.objects.get(id=rfc_results.rfc_lead.id)
    user_list = User.objects.filter(
        is_active=True,
        id__in=user_group.objects.filter(
            is_deleted=False,
            group_id__in=object_assignment.objects.filter(
                is_deleted=False,
                request_for_change_id=rfc_id,
            ).values('group_id')
        ).values('username_id')
    )

    # Context
    c = {
        'rfc_id': rfc_id,
        'rfc_results': serializers.serialize('json', [rfc_results]),
        'rfc_change_lead': serializers.serialize('json', [rfc_change_lead]),
        'user_list': serializers.serialize('json', user_list),
    }

    return c


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def rfc_change_task_list(request,rfc_id):
    """
    """
    change_task_results = change_task.objects.filter(
        is_deleted=False,
        request_for_change=rfc_id,
    ).order_by('change_task_start_date','change_task_end_date')

    # Send back JSON response
    return HttpResponse(serializers.serialize('json', change_task_results), content_type='application/json')


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


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def new_request_for_change_save(request):
    """

    :param request:
    :return:
    """

    # Check the user's permission

    # Get the form data
    form = NewRequestForChangeForm(request.POST)
    if not form.is_valid():
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


@login_required(login_url='login', redirect_field_name="")
def rfc_information(request,rfc_id):
    """

    :param request:
    :param rfc_id:
    :return:
    """
    # Get template
    t = loader.get_template('NearBeach/request_for_change/rfc_information.html')

    # Get context
    c = get_rfc_context(rfc_id)

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def rfc_information_save(request,rfc_id):
    """

    :param request:
    :param rfc_id:
    :return:
    """

    # PROGRAM IN PERMISSIONS
    
    # Get the form data
    form = RfcInformationSaveForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the request for change data
    update_rfc = request_for_change.objects.get(rfc_id=rfc_id)

    # Update the data
    update_rfc.rfc_title = form.cleaned_data['rfc_title']
    update_rfc.rfc_summary = form.cleaned_data['rfc_summary']
    update_rfc.rfc_type = form.cleaned_data['rfc_type']
    update_rfc.rfc_version_number = form.cleaned_data['rfc_version_number']
    update_rfc.rfc_implementation_start_date = form.cleaned_data['rfc_implementation_start_date']
    update_rfc.rfc_implementation_end_date = form.cleaned_data['rfc_implementation_end_date']
    update_rfc.rfc_implementation_release_date = form.cleaned_data['rfc_implementation_release_date']

    # Save the data
    update_rfc.save()
    
    # Return blank success
    return HttpResponse("")


@login_required(login_url='login', redirect_field_name="")
def rfc_readonly(request,rfc_id):
    """

    :param request:
    :param rfc_id:
    :return:
    """

    # Get template
    t = loader.get_template('NearBeach/request_for_change/rfc_readonly.html')

    # Get context
    c = get_rfc_context(rfc_id)

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def rfc_save_backout(request,rfc_id):
    """

    :param request:
    :return:
    """

    # Get the form data
    form = RfcModuleForm(request.POST) 
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the RFC in question
    update_rfc = request_for_change.objects.get(rfc_id=rfc_id)

    # Update the rfc
    update_rfc.rfc_backout_plan = form.cleaned_data['text_input']

    # Save
    update_rfc.save()

    return HttpResponse("")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def rfc_save_implementation(request,rfc_id):
    """
    """

    # Check user permissions

    # Get the form data
    form = RfcModuleForm(request.POST) 
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc in question
    update_rfc = request_for_change.objects.get(rfc_id=rfc_id)

    # Update the data
    update_rfc.rfc_implementation_plan = form.cleaned_data['text_input']

    #Save
    update_rfc.save()
    
    return HttpResponse("")

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
def rfc_save_risk(request, rfc_id):
    """
    """

    # CHECK USER PERMISSIONS

    # Get the form data
    form = RfcModuleForm(request.POST) 
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the RFC in question
    update_rfc = request_for_change.objects.get(rfc_id=rfc_id)

    # Fill in the data
    update_rfc.rfc_priority = form.cleaned_data['priority_of_change']
    update_rfc.rfc_risk = form.cleaned_data['risk_of_change']
    update_rfc.rfc_impact = form.cleaned_data['impact_of_change']
    update_rfc.rfc_risk_and_impact_analysis = form.cleaned_data['text_input']

    # Save the data
    update_rfc.save()

    # Return blank result
    return HttpResponse("")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def rfc_save_test(request,rfc_id):
    """
    """

    # Check user permissions

    # Get the form data
    form = RfcModuleForm(request.POST) 
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc in question
    update_rfc = request_for_change.objects.get(rfc_id=rfc_id)

    # Update the rfc's data
    update_rfc.rfc_test_plan = form.cleaned_data['text_input']

    # Save data
    update_rfc.save()

    return HttpResponse("")
