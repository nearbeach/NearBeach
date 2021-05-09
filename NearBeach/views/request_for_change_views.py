from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from NearBeach.decorators.check_user_permissions import check_user_permissions, check_rfc_permissions

from NearBeach.models import *
from NearBeach.forms import NewRequestForChangeForm, RfcModuleForm, RfcInformationSaveForm, NewChangeTaskForm, \
    UpdateRFCStatus


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


@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=3)
def new_request_for_change(request, *args, **kwargs):
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

    user_results = User.objects.filter(  # This should only be group leaders
        is_active=True,
    )

    # Context
    c = {
        'group_results': serializers.serialize('json', group_results),
        'user_results': serializers.serialize('json', user_results),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=3)
def new_request_for_change_save(request, *args, **kwargs):
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


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=1)
def rfc_change_task_list(request, rfc_id, *args, **kwargs):
    """
    """
    change_task_results = change_task.objects.filter(
        is_deleted=False,
        request_for_change=rfc_id,
    ).order_by('change_task_start_date', 'change_task_end_date')

    # Send back JSON response
    return HttpResponse(serializers.serialize('json', change_task_results), content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=2)
def rfc_deployment(request, rfc_id, *args, **kwargs):
    """

    :param request:
    :param rfc_id:
    :return:
    """
    # If rfc is not in draft mode - send user away
    rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
    if not rfc_results.rfc_status == 3:  # Approved
        return HttpResponseRedirect(reverse('rfc_readonly', args={rfc_id}))

    # Get template
    t = loader.get_template('NearBeach/request_for_change/rfc_deployment.html')

    # Get context
    c = get_rfc_context(rfc_id)

    return HttpResponse(t.render(c, request))



@require_http_methods(["POST"])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=2)
def rfc_new_change_task(request, rfc_id, *args, **kwargs):
    """

    :param request:
    :param rfc_id:
    :return:
    """

    # ADD IN USER PERMISSIONS

    # Place data into forms for validation
    form = NewChangeTaskForm(request.POST)
    if not form.is_valid():
        # Send user bad request
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_change_task = change_task(
        request_for_change=form.cleaned_data['request_for_change'],
        change_task_title=form.cleaned_data['change_task_title'],
        change_task_description=form.cleaned_data['change_task_description'],
        change_task_start_date=form.cleaned_data['change_task_start_date'],
        change_task_end_date=form.cleaned_data['change_task_end_date'],
        change_task_seconds=form.cleaned_data['change_task_seconds'],
        # change_task_assigned_user = form.cleaned_data['change_task_assigned_user'],
        # change_task_qa_user = form.cleaned_data['change_task_qa_user'],
        change_task_assigned_user=request.user,
        change_task_qa_user=request.user,
        change_task_required_by=form.cleaned_data['change_task_required_by'],
        is_downtime=form.cleaned_data['is_downtime'],
        change_task_status=1,
        change_user=request.user,
        creation_user=request.user,
    )
    submit_change_task.save()

    # Send back all the RFC change items
    change_item_results = change_task.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
    )

    # Get all the change task results and send it back
    change_task_results = change_task.objects.filter(
        is_deleted=False,
        request_for_change=rfc_id,
    ).order_by('change_task_start_date', 'change_task_end_date')

    # Send back JSON response
    return HttpResponse(serializers.serialize('json', change_task_results), content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=1)
def rfc_information(request, rfc_id, *args, **kwargs):
    """

    :param request:
    :param rfc_id:
    :return:
    """

    # If rfc is not in draft mode - send user away
    rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
    if not rfc_results.rfc_status == 1:  # Draft
        return HttpResponseRedirect(reverse('rfc_readonly', args={rfc_id}))

    # Get template
    t = loader.get_template('NearBeach/request_for_change/rfc_information.html')

    # Get context
    c = get_rfc_context(rfc_id)

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=2)
def rfc_information_save(request, rfc_id, *args, **kwargs):
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
@check_rfc_permissions(min_permission_level=1)
def rfc_readonly(request, rfc_id, *args, **kwargs):
    """

    :param request:
    :param rfc_id:
    :return:
    """

    # Get template
    t = loader.get_template('NearBeach/request_for_change/rfc_readonly.html')

    # Get context
    c = get_rfc_context(rfc_id)

    # Determine if the user is a group leader for ANY of the groups assigned to this rfc
    group_leader_count = object_assignment.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
        group_id__in=user_group.objects.filter(
            is_deleted=False,
            username_id=request.user,
            group_leader=True,
        ).values('group_id')
    ).count()

    # Add the group_leader_count to c dict
    c.update({'group_leader_count': group_leader_count})

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=2)
def rfc_save_backout(request, rfc_id, *args, **kwargs):
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
@check_rfc_permissions(min_permission_level=2)
def rfc_save_implementation(request, rfc_id, *args, **kwargs):
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

    # Save
    update_rfc.save()

    return HttpResponse("")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
@check_rfc_permissions(min_permission_level=2)
def rfc_save_risk(request, rfc_id, *args, **kwargs):
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
@check_rfc_permissions(min_permission_level=2)
def rfc_save_test(request, rfc_id, *args, **kwargs):
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


# Internal function
def rfc_status_approved(rfc_id, rfc_results, request):
    """
    Method
    ~~~~~~
    1. Gather all User's rfc_group_rfc_approvals - and approve
    2. Check if there are any waiting rfc_group_rfc_approvals left - if none, approve rfc
    :param request:
    :param rfc_results:
    :param rfc_id:
    :return:
    """
    # Get group results
    group_results = user_group.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Update all user's rfc_group_approvals to approved
    request_for_change_group_approval.objects.filter(
        is_deleted=False,
        rfc_id=rfc_id,
        group_id__in=group_results.values('group_id')
    ).update(approval=2)

    # Send off to check to make sure that the rfc status needs updating
    rfc_status_check_approval_status(rfc_id, rfc_results, group_results)

    return


# Internal function
def rfc_status_check_approval_status(rfc_id, rfc_results, group_results):
    """

    :param group_results:
    :param rfc_results:
    :param rfc_id:
    :return:
    """

    # Check all submitted group approvals to make sure that they are all approved - if they are, update the status.
    non_approved_group_approvals = request_for_change_group_approval.objects.filter(
        is_deleted=False,
        group_id__in=group_results.values('group_id'),
        rfc_id=rfc_id,
        approval=1,
    ).count()

    # If there are no waiting for approval results - we default up to approved
    if non_approved_group_approvals == 0:
        rfc_results.rfc_status = 3  # Approved value
        rfc_results.save()

        # Update all change tasks to approved
        change_task.objects.filter(
            is_deleted=False,
            request_for_change_id=rfc_id,
            change_task_status=2,
        ).update(change_task_status=3)

    return


# Internal function
def rfc_status_rejected(rfc_id, rfc_results):
    """

    :param rfc_results:
    :param rfc_id:
    :return:
    """
    # Update all user's rfc_group_approvals to approved
    request_for_change_group_approval.objects.filter(
        is_deleted=False,
        rfc_id=rfc_id,
    ).update(approval=3)

    # Reject who RFC
    rfc_results.rfc_status = 6
    rfc_results.save()

    # Reject all the change tasks
    change_task.objects.filter(
        is_deleted=False,
        rfc_id=rfc_id,
    ).update(change_task_status=6)

    return


# Internal function
def rfc_status_waiting_for_approval(rfc_id, rfc_results, request):
    """
    Method
    ~~~~~~
    1. Find all groups associated with the RFC
    2. Create a single row for all groups in the request_for_change_group_approval
    3. Check to see if there are any group leaders in said groups - or auto approve
    4. Check to see if all tasks are auto approved, if so - auto apprve the rfc :)
    :param request:
    :param rfc_results:
    :param rfc_id:
    :return:
    """

    # Get the group results
    group_results = group.objects.filter(
        is_deleted=False,
        group_id__in=object_assignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
            request_for_change_id=rfc_id,
        ).values('group_id')
    )

    # Place all change tasks into waiting
    change_task.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
        change_task_status=1,
    ).update(change_task_status=2)

    # Loop through the groups, create the group approval, and see if there are ANY group leaders
    for single_group in group_results:
        # Create the group_approval
        submit_group_approval = request_for_change_group_approval(
            rfc_id=rfc_id,
            group_id=single_group.group_id,
            change_user_id=request.user.id,
        )

        # Check to see if there are any group leaders
        group_leader_count = user_group.objects.filter(
            is_deleted=False,
            group_id=single_group.group_id,
            group_leader=True,
        ).count()

        if group_leader_count == 0:
            submit_group_approval.approval = 2
        else:
            submit_group_approval.approval = 1

        # Save the data
        submit_group_approval.save()

    rfc_status_check_approval_status(rfc_id, rfc_results, group_results)

    return


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_rfc_permissions(min_permission_level=2)
def rfc_update_status(request, rfc_id, *args, **kwargs):
    """
    Using a simple form, we determine which status we are going to update to - and apply the correct status.
    :param request:
    :param rfc_id:
    :return:
    """

    # Add in user permissions

    # Get the form data
    form = UpdateRFCStatus(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc
    rfc_update = request_for_change.objects.get(rfc_id=rfc_id)

    # Update the status
    rfc_update.rfc_status = int(form.cleaned_data['rfc_status'])
    rfc_update.save()

    # Depending on what the status is depends what to do
    status_dict = dict(RFC_STATUS)
    if status_dict[form.cleaned_data['rfc_status']] == 'Waiting for approval':
        rfc_status_waiting_for_approval(rfc_id, rfc_update, request)
    if status_dict[form.cleaned_data['rfc_status']] == 'Approved':
        rfc_status_approved(rfc_id, rfc_update, request)
    if status_dict[form.cleaned_data['rfc_status']] == 'Rejected':
        rfc_status_rejected(rfc_id, rfc_update)

    return HttpResponse("")
