import json, uuid, datetime

from django.shortcuts import get_object_or_404
from django.db.models import Max, Min

from NearBeach.forms import (
    NewRequestForChangeForm,
    RfcModuleForm,
    RfcInformationSaveForm,
    NewChangeTaskForm,
    UpdateChangeLeadForm,
    UpdateRFCStatus,
)
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions
from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus
from NearBeach.views.tools.internal_functions import get_all_groups, get_user_group_permission
from NearBeach.models import (
    RequestForChange,
    User,
    UserGroup,
    ObjectAssignment,
    Group,
    ChangeTask,
    RequestForChangeGroupApproval,
)
from NearBeach.views.theme_views import get_theme
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers


# Internal function
def get_rfc_change_task(rfc_id):
    """Obtains a list of change tasks for this particular RFC, along with any blocked information."""
    change_task_results = ChangeTask.objects.filter(
        is_deleted=False,
        request_for_change=rfc_id,
    ).order_by("change_task_start_date", "change_task_end_date").values()

    blocked_list = ObjectAssignment.objects.filter(
        Q(
            is_deleted=False,
            change_task_id__in=change_task_results.values('change_task_id'),
        )
        | Q(
            is_deleted=False,
            meta_object__in=change_task_results.values('change_task_id'),
        )
    ).values()

    # Convert data into json format
    change_task_results = json.dumps(list(change_task_results), cls=DjangoJSONEncoder)
    blocked_list = json.dumps(list(blocked_list), cls=DjangoJSONEncoder)

    # # Send back JSON response
    return JsonResponse({
        "change_tasks": json.loads(change_task_results),
        "blocked_list": json.loads(blocked_list),
    })


# Internal function
def get_rfc_context(rfc_id):
    """
    Using the rfc ID, it will extract the required context for the rfc_information and rfc_readonly
    :param rfc_id:
    :return:
    """
    # Get data
    rfc_results = RequestForChange.objects.get(rfc_id=rfc_id)
    rfc_change_lead = User.objects.filter(
        id=rfc_results.rfc_lead.id
    ).annotate(
        profile_picture=F('userprofilepicture__document_id__document_key')
    ).values(
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "profile_picture",
    )
    user_list = User.objects.filter(
        is_active=True,
        id__in=UserGroup.objects.filter(
            is_deleted=False,
            group_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                request_for_change_id=rfc_id,
            ).values("group_id"),
        ).values("username_id"),
    ).values(
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
    )

    # Convert from ORM to JSON
    rfc_change_lead = json.dumps(list(rfc_change_lead), cls=DjangoJSONEncoder)
    user_list = json.dumps(list(user_list), cls=DjangoJSONEncoder)

    # Context
    c = {
        "nearbeach_title": f"RFC {rfc_id}",
        "rfc_id": rfc_id,
        "rfc_results": serializers.serialize("json", [rfc_results]),
        "rfc_change_lead": rfc_change_lead,
        "user_list": user_list,
        "need_tinymce": True,
    }

    return c


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="request_for_change")
def new_request_for_change(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Get template
    t = loader.get_template("NearBeach/request_for_change/new_request_for_change.html")

    # Context
    c = {
        "need_tinymce": True,
        "group_results": get_all_groups(),
        "nearbeach_title": "New RFC",
        "user_group_permissions": get_user_group_permission(request.user, ["request_for_change"]),
        "theme": get_theme(request),
        "uuid": uuid.uuid4,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="request_for_change")
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

    # Setup the default dates for two weeks
    default_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Add two weeks onto each date
    default_date = default_date + datetime.timedelta(weeks=2)

    # Save the data
    rfc_submit = RequestForChange(
        change_user=request.user,
        creation_user=request.user,
        rfc_status=RequestForChangeStatus.DRAFT,
        rfc_title=form.cleaned_data["rfc_title"],
        rfc_summary=form.cleaned_data["rfc_summary"],
        rfc_type=form.cleaned_data["rfc_type"],
        rfc_implementation_start_date=default_date,
        rfc_implementation_end_date=default_date,
        rfc_implementation_release_date=default_date,
        rfc_version_number=form.cleaned_data["rfc_version_number"],
        rfc_lead=form.cleaned_data["rfc_lead"],
        rfc_priority=form.cleaned_data["rfc_priority"],
        rfc_risk=form.cleaned_data["rfc_risk"],
        rfc_impact=form.cleaned_data["rfc_impact"],
        rfc_risk_and_impact_analysis=form.cleaned_data["rfc_risk_and_impact_analysis"],
        rfc_implementation_plan=form.cleaned_data["rfc_implementation_plan"],
        rfc_backout_plan=form.cleaned_data["rfc_backout_plan"],
        rfc_test_plan=form.cleaned_data["rfc_test_plan"],
    )
    rfc_submit.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = Group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = ObjectAssignment(
            group_id=group_instance,
            request_for_change=rfc_submit,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(reverse("rfc_information", args=[rfc_submit.rfc_id]))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="request_for_change")
def rfc_change_task_list(request, rfc_id, *args, **kwargs):
    # Return data from function get_rfc_change_task
    return get_rfc_change_task(rfc_id)


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_deployment(request, rfc_id, *args, **kwargs):
    """
    :param request:
    :param rfc_id:
    :return:
    """
    # If rfc is not in draft mode - send user away
    rfc_results = RequestForChange.objects.get(rfc_id=rfc_id)
    if not rfc_results.rfc_status == 3:  # Approved
        return HttpResponseRedirect(reverse("rfc_readonly", args={rfc_id}))

    # Get template
    t = loader.get_template("NearBeach/request_for_change/rfc_deployment.html")

    # Get context
    c = get_rfc_context(rfc_id)

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="request_for_change")
def rfc_get_approval_users(request, rfc_id, *args, **kwargs):
    """
    :param request:
    :param rfc_id:
    :return:
    """
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        group_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            request_for_change_id=rfc_id,
        ).values('group_id'),
        group_leader=True,
    )

    # Get the user details
    user_results = User.objects.filter(
        id__in=user_group_results.values("username_id")
    ).annotate(
        profile_picture=F('userprofilepicture__document_id__document_key')
    ).values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "profile_picture",
    )

    # Send the data to the user
    data_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(data_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_new_change_task(request, rfc_id, *args, **kwargs):
    """
    :param request:
    :param rfc_id:
    :return:
    """
    # Place data into forms for validation
    form = NewChangeTaskForm(request.POST)
    if not form.is_valid():
        # Send user bad request
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_change_task = ChangeTask(
        request_for_change=form.cleaned_data["request_for_change"],
        change_task_title=form.cleaned_data["change_task_title"],
        change_task_start_date=form.cleaned_data["change_task_start_date"],
        change_task_end_date=form.cleaned_data["change_task_end_date"],
        change_task_seconds=form.cleaned_data["change_task_seconds"],
        change_task_assigned_user=form.cleaned_data["change_task_assigned_user"],
        change_task_qa_user=form.cleaned_data["change_task_qa_user"],
        change_task_status=1,
        change_user=request.user,
        creation_user=request.user,
    )
    submit_change_task.save()

    # Update the RFC's start and end date, based off the change tasks
    update_rfc_dates(rfc_id)

    # # Get all the change task results and send it back
    return get_rfc_change_task(rfc_id)


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="request_for_change")
def rfc_information(request, rfc_id, *args, **kwargs):
    """
    :param request:
    :param rfc_id:
    :return:
    """
    # If rfc is not in draft mode - send user away
    rfc_results = RequestForChange.objects.filter(is_deleted=False)
    rfc_results = get_object_or_404(rfc_results, rfc_id=rfc_id)
    if not rfc_results.rfc_status == RequestForChangeStatus.DRAFT or kwargs["user_level"] == 1:  # Draft
        return HttpResponseRedirect(reverse("rfc_readonly", args=[rfc_id]))

    # Get template
    t = loader.get_template("NearBeach/request_for_change/rfc_information.html")

    # Get context
    c = get_rfc_context(rfc_id)
    c["user_level"] = kwargs["user_level"]
    c["theme"] = get_theme(request)

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
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
    update_rfc = RequestForChange.objects.get(rfc_id=rfc_id)

    # Update the data
    update_rfc.rfc_title = form.cleaned_data["rfc_title"]
    update_rfc.rfc_summary = form.cleaned_data["rfc_summary"]
    update_rfc.rfc_type = form.cleaned_data["rfc_type"]
    update_rfc.rfc_version_number = form.cleaned_data["rfc_version_number"]
    update_rfc.rfc_implementation_start_date = form.cleaned_data[
        "rfc_implementation_start_date"
    ]
    update_rfc.rfc_implementation_end_date = form.cleaned_data[
        "rfc_implementation_end_date"
    ]
    update_rfc.rfc_implementation_release_date = form.cleaned_data[
        "rfc_implementation_release_date"
    ]

    # Save the data
    update_rfc.save()

    # Return blank success
    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="request_for_change")
def rfc_readonly(request, rfc_id, *args, **kwargs):
    """
    :param request:
    :param rfc_id:
    :return:
    """
    # Get template
    t = loader.get_template("NearBeach/request_for_change/rfc_readonly.html")

    # Get context
    c = get_rfc_context(rfc_id)

    # Determine if the user is a group leader for ANY of the groups assigned to this rfc
    group_leader_count = ObjectAssignment.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
        group_id__in=UserGroup.objects.filter(
            is_deleted=False,
            username_id=request.user,
            group_leader=True,
        ).values("group_id"),
    ).count()

    # Add the group_leader_count to c dict
    c.update({"group_leader_count": group_leader_count})
    c["user_level"] = kwargs["user_level"]
    c["theme"] = get_theme(request)

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
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
    update_rfc = RequestForChange.objects.get(rfc_id=rfc_id)

    # Update the rfc
    update_rfc.rfc_backout_plan = form.cleaned_data["text_input"]

    # Save
    update_rfc.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_save_implementation(request, rfc_id, *args, **kwargs):
    """ """
    # Check user permissions

    # Get the form data
    form = RfcModuleForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc in question
    update_rfc = RequestForChange.objects.get(rfc_id=rfc_id)

    # Update the data
    update_rfc.rfc_implementation_plan = form.cleaned_data["text_input"]

    # Save
    update_rfc.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_save_risk(request, rfc_id, *args, **kwargs):
    """ """
    # CHECK USER PERMISSIONS

    # Get the form data
    form = RfcModuleForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the RFC in question
    update_rfc = RequestForChange.objects.get(rfc_id=rfc_id)

    # Fill in the data
    update_rfc.rfc_priority = form.cleaned_data["priority_of_change"]
    update_rfc.rfc_risk = form.cleaned_data["risk_of_change"]
    update_rfc.rfc_impact = form.cleaned_data["impact_of_change"]
    update_rfc.rfc_risk_and_impact_analysis = form.cleaned_data["text_input"]

    # Save the data
    update_rfc.save()

    # Return blank result
    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_save_test(request, rfc_id, *args, **kwargs):
    """ """
    # Check user permissions
    # Get the form data
    form = RfcModuleForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc in question
    update_rfc = RequestForChange.objects.get(rfc_id=rfc_id)

    # Update the rfc's data
    update_rfc.rfc_test_plan = form.cleaned_data["text_input"]

    # Save data
    update_rfc.save()

    return HttpResponse("")


# Internal function
def rfc_status_approved(rfc_id, rfc_results, request):
    """
    Method
    ~~~~~~
    1. Gather all User's rfc_group_rfc_approvals - and approve
    2. Check if there are any waiting rfc_group_rfc_approvals left -
    if none, approve rfc
    :param request:
    :param rfc_results:
    :param rfc_id:
    :return:
    """
    # Get group results
    group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Update all user's rfc_group_approvals to approved
    RequestForChangeGroupApproval.objects.filter(
        is_deleted=False, rfc_id=rfc_id, group_id__in=group_results.values("group_id")
    ).update(approval=2)

    # Send off to check to make sure that the rfc status needs updating
    rfc_status_check_approval_status(rfc_id, rfc_results, group_results)


# Internal function
def rfc_status_check_approval_status(rfc_id, rfc_results, group_results):
    """
    :param group_results:
    :param rfc_results:
    :param rfc_id:
    :return:
    """
    # Check all submitted group approvals to make sure that they are all approved -
    # if they are, update the status.
    non_approved_group_approvals = RequestForChangeGroupApproval.objects.filter(
        is_deleted=False,
        group_id__in=group_results.values("group_id"),
        rfc_id=rfc_id,
        approval=1,
    ).count()

    # If there are no waiting for approval results - we default up to approved
    print(f"NON APPROVED: {non_approved_group_approvals}")
    if non_approved_group_approvals == 0:
        rfc_results.rfc_status = RequestForChangeStatus.APPROVED
        rfc_results.save()

        print("GOT IN HERE!")

        # Update all change tasks to approved
        ChangeTask.objects.filter(
            is_deleted=False,
            request_for_change_id=rfc_id,
        ).update(change_task_status=3)


# Internal function
def rfc_status_rejected(rfc_id, _):
    """
    :param rfc_results:
    :param rfc_id:
    :return:
    """
    # Update all user's rfc_group_approvals to approved
    RequestForChangeGroupApproval.objects.filter(
        is_deleted=False,
        rfc_id=rfc_id,
    ).update(approval=3)

    # Reject who RFC
    # rfc_results.rfc_status = 6
    # rfc_results.save()

    # Reject all the change tasks
    ChangeTask.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
    ).update(change_task_status=6)


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
    group_results = Group.objects.filter(
        is_deleted=False,
        group_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
            request_for_change_id=rfc_id,
        ).values("group_id"),
    )

    # Place all change tasks into waiting
    print(f"\n\nRFC ID: {rfc_id}\nARGH\n\n")
    ChangeTask.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id,
    ).update(change_task_status=2)

    # Loop through the groups, create the group approval,
    # and see if there are ANY group leaders
    for single_group in group_results:
        # Create the group_approval
        submit_group_approval = RequestForChangeGroupApproval(
            rfc_id=rfc_id,
            group_id=single_group.group_id,
            change_user_id=request.user.id,
        )

        # Check to see if there are any group leaders
        group_leader_count = UserGroup.objects.filter(
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


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_update_change_lead(request, rfc_id, *args, **kwargs):
    # Get the form data
    form = UpdateChangeLeadForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the rfc
    rfc_update = RequestForChange.objects.get(rfc_id=rfc_id)
    rfc_update.rfc_lead = form.cleaned_data['username']
    rfc_update.save()

    # Get the change lead information
    change_lead_results = User.objects.filter(
        username = form.cleaned_data['username']
    ).annotate(
        profile_picture=F('userprofilepicture__document_id__document_key')
    ).values(
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "profile_picture",
    )

    # Setup the data to send back
    change_lead_results = json.dumps(list(change_lead_results), cls=DjangoJSONEncoder)

    return_data = {
        "change_lead_results": json.loads(change_lead_results),
    }

    return JsonResponse(return_data)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="request_for_change")
def rfc_update_status(request, rfc_id, *args, **kwargs):
    """
    Using a simple form, we determine which status we are going to update to
    and apply the correct status.
    :param request:
    :param rfc_id:
    :return:
    """
    form = UpdateRFCStatus(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the rfc
    rfc_update = RequestForChange.objects.get(rfc_id=rfc_id)

    # Update the status
    rfc_update.rfc_status = form.cleaned_data["rfc_status"]
    rfc_update.save()

    # Depending on what the status is depends what to do
    # status_dict = dict(RFC_STATUS)
    rfc_status = str(form.cleaned_data["rfc_status"])
    if rfc_status == "Waiting for approval":
        rfc_status_waiting_for_approval(rfc_id, rfc_update, request)
    if rfc_status == "Approved":
        rfc_status_approved(rfc_id, rfc_update, request)
    if rfc_status == "Rejected":
        rfc_status_rejected(rfc_id, rfc_update)

    return HttpResponse("")


# Internal function
def update_rfc_dates(rfc_id):
    """
    Will look up all the change tasks associated with this rfc, and update the start and end date using the min and max
    from the change tasks.
    """
    rfc_results = RequestForChange.objects.get(rfc_id=rfc_id)

    # Obtain the delta between the end date and the release date
    delta = abs(rfc_results.rfc_implementation_release_date - rfc_results.rfc_implementation_end_date)

    # Obtain all the change tasks and find the min and max date of all
    change_task_results = ChangeTask.objects.filter(
        is_deleted=False,
        request_for_change_id=rfc_id
    )

    # If there are no change tasks associated with this rfc. Just return.
    if len(change_task_results) == 0:
        return

    # Apply the dates
    start_date = change_task_results.aggregate(
        Min("change_task_start_date")
    )["change_task_start_date__min"]

    end_date = change_task_results.aggregate(
        Max("change_task_end_date")
    )["change_task_end_date__max"]

    release_date = end_date + delta

    # Update the RFC
    rfc_results.rfc_implementation_start_date=start_date
    rfc_results.rfc_implementation_end_date=end_date
    rfc_results.rfc_implementation_release_date=release_date

    rfc_results.save()

    return
