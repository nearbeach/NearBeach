from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Value, F

from NearBeach.models import (
    Project,
    RequirementItem,
    Sprint,
    SprintObjectAssignment,
    Task,
)

import json


def gantt_data_get_data(request, destination, location_id, *args, **kwargs):
    # For the initial proof of concept, we are only dealing with sprints
    if destination != "sprint":
        return HttpResponseBadRequest("Sorry, object not supported at the moment")

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
        status=F('project_status'),
        status_id=F('project_status_id'),
        start_date=F('project_start_date'),
        end_date=F('project_end_date'),
        object_type=Value("project"),
    ).values(
        'title',
        'status',
        'status_id',
        'start_date',
        'end_date',
        'object_type',
    )

    task_results = Task.objects.filter(
        is_deleted=False,
        task_id__in=sprint_object_assignment_results.filter(
            task_id__isnull=False,
        ).values("task_id")
    ).annotate(
        title=F('task_short_description'),
        status=F('task_status'),
        status_id=F('task_status_id'),
        start_date=F('task_start_date'),
        end_date=F('task_end_date'),
        object_type=Value("project"),
    ).values(
        'title',
        'status',
        'status_id',
        'start_date',
        'end_date',
        'object_type',
    )

    # Union the data and send back to user
    results = project_results.union(
        task_results
    ).values(
        'title',
        'status',
        'status_id',
        'start_date',
        'end_date',
        'object_type',
    )

    results = json.dumps(list(results), cls=DjangoJSONEncoder)

    return JsonResponse(json.loads(results), safe=False)
