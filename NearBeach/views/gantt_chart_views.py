from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Value, F

from NearBeach.forms import GanttDataUpdateDataForm
from NearBeach.models import (
    Project,
    RequirementItem,
    Sprint,
    SprintObjectAssignment,
    Task, ListOfRequirementItemStatus, ListOfProjectStatus, ListOfTaskStatus,
)
from NearBeach.decorators.check_user_permissions.gantt_chart_permissions import (
    check_gantt_chart_permissions_with_destination,
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
}


@check_gantt_chart_permissions_with_destination(min_permission_level=1)
def gantt_data_get_data(request, destination, location_id, *args, **kwargs):
    # Get the object results
    object_results = get_object_results(location_id)
    status_results = get_status_results()

    results = {
        "object_results": json.loads(object_results),
        "status_results": status_results,
    }

    return JsonResponse(
        results,
        safe=False,
    )


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
    setattr(update_object, gantt_object_dict["end_date"], form.cleaned_data["end_date"])
    setattr(update_object, gantt_object_dict["start_date"], form.cleaned_data["start_date"])
    setattr(update_object, gantt_object_dict["status_id"], form.cleaned_data["status_id"])

    # Save the updates
    update_object.save()

    return HttpResponse("")


# Internal Function
def get_object_results(location_id):

    # Import all connected objects
    sprint_object_assignment_results = SprintObjectAssignment.objects.filter(
        is_deleted=False,
        sprint_id=location_id,
    )

    # requirement_item_results = RequirementItem.objects.filter(
    #     is_deleted=False,
    #     requirement_item_id__in=sprint_object_assignment_results.filter(
    #         requirement_item__isnull=False,
    #     ).values("requirement_item_id"),
    # ).annotate(
    #     title=requirement_item_title,
    #     status=requirement_item_status,
    #     status_id=requirement_item_status_id,
    #     start_date=requirement_item_
    # )

    project_results = Project.objects.filter(
        is_deleted=False,
        project_id__in=sprint_object_assignment_results.filter(
            project_id__isnull=False,
        ).values("project_id"),
    ).annotate(
        title=F('project_name'),
        status_id=F('project_status_id'),
        higher_order_status=F('project_status__project_higher_order_status'),
        start_date=F('project_start_date'),
        end_date=F('project_end_date'),
        object_type=Value("project"),
        object_id=F("project_id"),
    ).values(
        'title',
        'status_id',
        'higher_order_status',
        'start_date',
        'end_date',
        'object_type',
        'object_id',
    )

    task_results = Task.objects.filter(
        is_deleted=False,
        task_id__in=sprint_object_assignment_results.filter(
            task_id__isnull=False,
        ).values("task_id")
    ).annotate(
        title=F('task_short_description'),
        status_id=F('task_status_id'),
        higher_order_status=F('task_status__task_higher_order_status'),
        start_date=F('task_start_date'),
        end_date=F('task_end_date'),
        object_type=Value("task"),
        object_id=F("task_id")
    ).values(
        'title',
        'status_id',
        'higher_order_status',
        'start_date',
        'end_date',
        'object_type',
        'object_id',
    )

    # Union the data and send back to user
    object_results = project_results.union(
        task_results
    ).values(
        'title',
        'status_id',
        'higher_order_status',
        'start_date',
        'end_date',
        'object_type',
        'object_id',
    )

    # Just return the json dumps
    return json.dumps(list(object_results), cls=DjangoJSONEncoder)


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
