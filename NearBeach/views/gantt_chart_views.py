from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import F
from django.db import connection

from NearBeach.forms import GanttDataUpdateDataForm
from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfProjectStatus,
    ListOfTaskStatus,
    Project,
    RequirementItem,
    Task,
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
    "requirement_item": {
        "object": RequirementItem,
        "end_date": "",
        "start_date": "",
        "status_id": "requirement_item_status_id",
    },
}


@check_gantt_chart_permissions_with_destination(min_permission_level=1)
def gantt_data_get_data(request, destination, location_id, *args, **kwargs):
    # Check to make sure the destination is a sprint
    if not destination == "sprint":
        return HttpResponseBadRequest("Not a sprint")

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
    setattr(update_object, gantt_object_dict["status_id"], form.cleaned_data["status_id"])
    if destination != "requirement_item":
        setattr(update_object, gantt_object_dict["end_date"], form.cleaned_data["end_date"])
        setattr(update_object, gantt_object_dict["start_date"], form.cleaned_data["start_date"])

    # Save the updates
    update_object.save()

    return HttpResponse("")


# Internal Function
def get_object_results(location_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH TmpTable(
                  sprint_object_assignment_id
                , project_id
                , requirement_item_id
                , sprint_id_id
                , task_id
            ) AS (
                SELECT DISTINCT
                  sprint_object_assignment_id
                , project_id
                , requirement_item_id
                , sprint_id_id
                , task_id
                FROM [NearBeach_sprintobjectassignment]
                WHERE 1=1
                AND is_deleted = 0
                AND sprint_id_id = %s
            )

            SELECT DISTINCT
              P.project_name AS 'title'
            , P.project_description AS 'description'
            , P.project_status_id AS 'status_id'
            , PS.project_higher_order_status AS 'higher_order_status'
            , P.project_start_date AS 'start_date'
            , P.project_end_date AS 'end_date'
            , 'project' AS 'object_type'
            , P.project_id AS 'object_id'
            , OA.parent_link AS 'parent_object_type'
            , OA.requirement_item_id AS 'parent_object_id'
            FROM [NearBeach_project] AS P LEFT JOIN [NearBeach_listofprojectstatus] PS
                ON PS.project_status_id = P.project_status_id
                LEFT OUTER JOIN [NearBeach_objectassignment] OA
                ON OA.project_id = P.project_id
                AND OA.link_relationship = 'Subobject'
                AND OA.parent_link IN ('requirement_item')
                AND OA.requirement_item_id IN (
                    SELECT requirement_item_id FROM TmpTable
                )
                AND OA.is_deleted = 0
                
            WHERE P.project_id IN (
                SELECT project_id FROM TmpTable
            )


            UNION


            SELECT
              T.task_short_description AS 'title'
            , T.task_long_description AS 'description'
            , T.task_status_id AS 'status_id'
            , TS.task_higher_order_status AS 'higher_order_status'
            , T.task_start_date AS 'start_date'
            , T.task_end_date AS 'end_date'
            , 'task' AS 'object_type'
            , T.task_id AS 'object_id'
            , OA.parent_link AS 'parent_object_type'
            , CASE OA.parent_link
                WHEN 'requirement_item' THEN OA.requirement_item_id
                WHEN 'project' THEN OA.project_id
                ELSE ''
            END AS 'parent_object_id'
            FROM [NearBeach_task] T LEFT JOIN [NearBeach_listoftaskstatus] TS
                ON TS.task_status_id = T.task_status_id
                LEFT OUTER JOIN [NearBeach_objectassignment] OA
                ON OA.task_id = T.task_id
                AND OA.link_relationship = 'Subobject'
                AND OA.parent_link IN ('requirement_item', 'project')
                AND (
                    OA.requirement_id IN (
                        SELECT requirement_id FROM TmpTable
                    )
                    OR OA.project_id IN (
                        SELECT project_id FROM TmpTable
                    )
                )
                AND OA.is_deleted = 0

            WHERE T.task_id IN (
                SELECT task_id FROM TmpTable
            )


            UNION


            SELECT DISTINCT
              RI.requirement_item_title AS 'title'
            , RI.requirement_item_scope AS 'description'
            , RI.requirement_item_status_id AS 'status_id'
            , RIS.requirement_item_higher_order_status AS 'higher_order_status'
            , '' AS 'start_date'
            , '' AS 'end_date'
            , 'requirement_item' AS 'object_type'
            , RI.requirement_item_id AS 'object_id'
            , '' AS 'object_id'
            , '' AS 'parent_object_type'
            FROM [NearBeach_requirementitem] RI LEFT JOIN [NearBeach_listofrequirementitemstatus] RIS
                ON RIS.requirement_item_status_id = RI.requirement_item_status_id
            WHERE RI.requirement_item_id IN (
                SELECT requirement_item_id FROM TmpTable
            ) 
            """,
           [location_id]
        )
        # object_results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        object_results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
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
