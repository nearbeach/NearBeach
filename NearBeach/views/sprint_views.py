from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader

import json

from NearBeach.forms import NewSprintForm
from NearBeach.models import Sprint, SprintObjectAssignment, RequirementItem, Project, Task
from NearBeach.views.theme_views import get_theme


def delete_sprint(request, sprint_id):
    Sprint.objects.filter(
        sprint_id=sprint_id
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


def list_assigned_sprints(request, destination, location_id, *args, **kwargs):
    return HttpResponse("")


def list_child_sprints(request, destination, location_id, *args, **kwargs):
    sprint_results = Sprint.objects.filter(
        is_deleted=False,
        **{F"{destination}_id": location_id},
    ).values(
        "sprint_id",
        "sprint_name",
        "total_story_points",
        "completed_story_points",
        "sprint_status",
        "sprint_start_date",
        "sprint_end_date",
    )

    sprint_results = json.dumps(list(sprint_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(sprint_results), safe=False)


def new_sprint(request, destination, location_id):
    form = NewSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data in a new object
    sprint_submit = Sprint(
        sprint_name=form.cleaned_data["sprint_name"],
        sprint_start_date=form.cleaned_data["sprint_start_date"],
        sprint_end_date=form.cleaned_data["sprint_end_date"],
        change_user=request.user,
        **{F"{destination}_id": location_id, },
    )
    sprint_submit.save()

    return JsonResponse({'id': sprint_submit.sprint_id, })


def sprint_information(request, sprint_id, *args, **kwargs):
    # Get the template
    t = loader.get_template("NearBeach/sprints/sprint_information.html")

    sprint_results = Sprint.objects.filter(
        sprint_id=sprint_id,
    ).values(
        "sprint_id",
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


