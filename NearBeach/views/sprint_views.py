from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader

import json

from django.views.decorators.http import require_http_methods

from NearBeach.forms import NewSprintAssignmentForm, NewSprintForm, AddObjectToSprintForm, RemoveSprintForm
from NearBeach.models import Sprint, SprintObjectAssignment, RequirementItem, Project, Task, ObjectAssignment, UserGroup
from NearBeach.views.theme_views import get_theme

from NearBeach.views.tools.lookup_functions import (
    lookup_project,
    lookup_requirement_item,
    lookup_task,
)

from NearBeach.decorators.check_user_permissions.sprint_permissions import (
    check_sprint_permission_with_sprint,
    check_sprint_permissions_with_destination,
)

from NearBeach.decorators.check_user_permissions.object_permissions import check_user_generic_permissions

LOOKUP_FUNCS = {
    "project": lookup_project,
    "task": lookup_task,
    "requirement_item": lookup_requirement_item,
}


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def add_object_to_sprint(request, destination, location_id, *args, **kwargs):
    if not destination == "sprint":
        return HttpResponseBadRequest("Sorry - object not allowed")

    # Get the data
    form = AddObjectToSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Loop through the above form, only looking at the fields in the object type
    for object_type in ["requirement_item", "project", "task"]:
        for row in request.POST.getlist(object_type):
            submit_object_assignment = SprintObjectAssignment(
                **{F"{object_type}_id": row},
                change_user=request.user,
                sprint_id_id=location_id,
            )
            submit_object_assignment.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def add_sprint_to_object(request, destination, location_id, *args, **kwargs):
    """
    User currently on an object information page. They have selected this object be added to an existing sprint.
    """
    form = NewSprintAssignmentForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    submit_sprint_assignment = SprintObjectAssignment(
        sprint_id=form.cleaned_data["sprint_id"],
        **{F"{destination}_id": location_id},
        change_user=request.user,
    )
    submit_sprint_assignment.save()

    # Return the updated sprint list
    sprint_results = get_assigned_sprints(destination, location_id)
    return JsonResponse(json.loads(sprint_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def delete_sprint(request, sprint_id, *args, **kwargs):
    Sprint.objects.filter(
        sprint_id=sprint_id
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def finish_sprint(request, sprint_id, *args, **kwargs):
    Sprint.objects.filter(
        sprint_id=sprint_id,
        sprint_status="Current",
    ).update(
        sprint_status="Finished"
    )

    return HttpResponse("")


# Internal function
def get_assigned_sprints(destination, location_id, *args, **kwargs):
    sprint_results = Sprint.objects.filter(
        is_deleted=False,
        sprint_id__in=SprintObjectAssignment.objects.filter(
            is_deleted=False,
            **{F"{destination}_id": location_id},
        ).values("sprint_id")
    ).values(
        "sprint_id",
        "sprint_name",
        "total_story_points",
        "completed_story_points",
        "sprint_status",
        "sprint_start_date",
        "sprint_end_date",
    )

    return json.dumps(list(sprint_results), cls=DjangoJSONEncoder)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_generic_permissions(min_permission_level=1)
def list_assigned_sprints(request, destination, location_id, *args, **kwargs):
    sprint_results = get_assigned_sprints(destination, location_id)
    return JsonResponse(json.loads(sprint_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permissions_with_destination(1)
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


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
# @check_sprint_permissions_with_destination(1)
@check_sprint_permission_with_sprint(min_permission_level=1)
def potential_object_list(request, destination, location_id, object_lookup, *args, **kwargs):
    """
    Used to get a list of potential objects that can be assigned to a sprint.
    """
    if not destination == "sprint":
        return HttpResponseBadRequest("Object has to be a sprint")

    # Get user groups
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
        group_id__isnull=False,
    ).values("group_id")

    if object_lookup not in LOOKUP_FUNCS:
        return HttpResponseBadRequest("Sorry - but that object lookup does not exist")

    # Get the data dependent on the object lookup
    data_results = LOOKUP_FUNCS[object_lookup](user_group_results, "object_assignment_id", 0)

    # Send the data to the user
    data_results = json.dumps(list(data_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(data_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permissions_with_destination(2)
def new_sprint(request, destination, location_id, *args, **kwargs):
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


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def remove_sprint(request, destination, location_id, *args, **kwargs):
    form = RemoveSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)


    SprintObjectAssignment.objects.filter(
        **{F"{destination}_id": location_id},
        sprint_id=form.cleaned_data["sprint_id"],
    ).update(
        is_deleted=True,
    )

    sprint_results = get_assigned_sprints(destination, location_id)
    return JsonResponse(json.loads(sprint_results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(1)
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
        "user_level": kwargs["user_level"],
        "theme": get_theme(request),

        # TEMP CODE
        "requirement_item_results": serializers.serialize("json", requirement_item_results),
        "project_results": serializers.serialize("json", project_results),
        "task_results": serializers.serialize("json", task_results),
        # END TEMP CODE
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
def sprint_list(request):
    """
    Sends back a list of all potential sprints the user has access too. Designed so users can select which sprint an
    object can be assigned too
    """
    object_assignment_results = ObjectAssignment.objects.filter(
        Q(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values('group_id'),
        ) & Q(
            Q(project_id__isnull=False) |
            Q(requirement_id__isnull=False)
        )
    )

    # Using the object assignment results - we can determine which sprints the user has access too
    sprint_results = Sprint.objects.filter(
        Q(
            is_deleted=False,
            project_id__in=object_assignment_results.values("project_id"),
        ) |
        Q(
            is_deleted=False,
            requirement_id__in=object_assignment_results.values("requirement_id"),
        )
    ).exclude(
        sprint_status="Finished",
    ).values(
        "sprint_id",
        "sprint_name",
        "sprint_start_date",
        "sprint_end_date",
    )

    sprint_results = json.dumps(list(sprint_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(sprint_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def start_sprint(request, sprint_id, *args, **kwargs):
    Sprint.objects.filter(
        sprint_id=sprint_id,
        sprint_status="Draft",
    ).update(
        sprint_status="Current",
    )

    return HttpResponse("")
