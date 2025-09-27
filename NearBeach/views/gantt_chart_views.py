from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import F

from NearBeach.forms import GanttDataUpdateDataForm
from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfProjectStatus,
    ListOfTaskStatus,
    Project,
    RequirementItem,
    Task,
)
from NearBeach.decorators.check_user_permissions.object_permissions import (
    check_user_generic_permissions,
)

import json


GANTT_DATA_UPDATE_STRUCTURE = {
    # REQUIREMENT ITEMS REQUIRE DATES FIRST
    "project": {
        "object": Project,
        "end_date": "project_end_date",
        "start_date": "project_start_date",
        "status_id": "project_status_id",
    },
    "task": {
        "object": Task,
        "end_date": "task_end_date",
        "start_date": "task_start_date",
        "status_id": "task_status_id",
    },
    "requirement_item": {
        "object": RequirementItem,
        "end_date": "",
        "start_date": "",
        "status_id": "requirement_item_status_id",
    },
}


@check_user_generic_permissions(min_permission_level=2)
def gantt_data_update_data(request, destination, location_id, *args, **kwargs):
    # Check the form data
    form = GanttDataUpdateDataForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Check the objects - use GANTT_DATA_UPDATE_STRUCTURE dict to get the correct object
    gantt_object_dict = GANTT_DATA_UPDATE_STRUCTURE[destination]
    update_object = gantt_object_dict["object"].objects.filter(pk=location_id)

    # If there are no results - send back bad request
    if len(update_object) == 0:
        return HttpResponseBadRequest("No object found. Error")

    # Grab just the first object to update
    update_object = update_object.first()

    # Update the object
    setattr(update_object, gantt_object_dict["status_id"], form.cleaned_data["status_id"])
    if destination != "requirement_item":
        setattr(update_object, gantt_object_dict["end_date"], form.cleaned_data["end_date"])
        setattr(update_object, gantt_object_dict["start_date"], form.cleaned_data["start_date"])

    # Save the updates
    update_object.save()

    return HttpResponse("")


# Internal function
def get_status_results():
    # Requirement Item
    # Project
    # Task
    requirement_item_status_results = ListOfRequirementItemStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F('requirement_item_status_id'),
        label=F('requirement_item_status'),
        higher_order_status=F('requirement_item_higher_order_status'),
    ).order_by(
        'requirement_item_status_sort_order',
    ).values(
       'value',
       'label',
       'higher_order_status',
    )

    project_status_results = ListOfProjectStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F('project_status_id'),
        label=F('project_status'),
        higher_order_status=F('project_higher_order_status'),
    ).order_by(
        'project_status_sort_order',
    ).values(
        'value',
        'label',
        'higher_order_status',
    )

    task_status_results = ListOfTaskStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F('task_status_id'),
        label=F('task_status'),
        higher_order_status=F('task_higher_order_status'),
    ).order_by(
        'task_status_sort_order',
    ).values(
        'value',
        'label',
        'higher_order_status',
    )

    # Convert the data to json format
    requirement_item_status_results = json.dumps(
        list(requirement_item_status_results),
        cls=DjangoJSONEncoder,
    )

    project_status_results = json.dumps(
        list(project_status_results),
        cls=DjangoJSONEncoder,
    )

    task_status_results = json.dumps(
        list(task_status_results),
        cls=DjangoJSONEncoder,
    )

    return {
        "requirement_item": json.loads(requirement_item_status_results),
        "project": json.loads(project_status_results),
        "task": json.loads(task_status_results),
    }
