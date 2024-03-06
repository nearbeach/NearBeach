from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader

import json

from NearBeach.models import Sprint, SprintObjectAssignment, RequirementItem, Project, Task
from NearBeach.views.theme_views import get_theme


def delete_sprint(request, sprint_id):
    return HttpResponse("")


def list_sprints(request, destination, location_id):
    return HttpResponse("")


def new_sprint(request, destination, location_id):
    return HttpResponse("")


def sprint_information(request, sprint_id, *args, **kwargs):
    # Get the template
    t = loader.get_template("NearBeach/sprints/sprint_information.html")

    sprint_results = Sprint.objects.filter(
        sprint_id=sprint_id,
    ).values(
        "completed_story_points",
        "project",
        "requirement",
        "sprint_name",
        "sprint_start_date",
        "sprint_status",
        "total_story_points",
    )

    # Import all connected objects
    sprint_object_assignment_results = SprintObjectAssignment.objects.filter(
        is_deleted=False,
        sprint_id=sprint_id,
    )

    requirement_item_results = RequirementItem.objects.filter(
        is_deleted=False,
        requirement_item_id__in=sprint_object_assignment_results.filter(
            requirement_item__isnull=False,
        ).values("requirement_item_id"),
    )

    project_results = Project.objects.filter(
        is_deleted=False,
        project_id__in=sprint_object_assignment_results.filter(
            project_id__isnull=False,
        ).values("project_id"),
    )

    task_results = Task.objects.filter(
        is_deleted=False,
        task_id__in=sprint_object_assignment_results.filter(
            task_id__isnull=False,
        ).values("task_id")
    )

    c = {
        "nearbeach_title": f"Sprint Information {sprint_id}",
        "need_tinymce": False,
        "sprint_results": json.dumps(list(sprint_results), cls=DjangoJSONEncoder),
        "user_level": 4, #TODO: Fix this - as we need to check the permissions
        "theme": get_theme(request),

        # TEMP CODE
        "requirement_item_results": serializers.serialize("json", requirement_item_results),
        "project_results": serializers.serialize("json", project_results),
        "task_results": serializers.serialize("json", task_results),
        # END TEMP CODE
    }

    return HttpResponse(t.render(c, request))


def sprint_information_save(request, sprint_id):
    return HttpResponse("")


