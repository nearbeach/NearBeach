from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.template import loader

import json

from django.views.decorators.http import require_http_methods

from NearBeach.forms import (
    NewSprintAssignmentForm,
    NewSprintForm,
    AddObjectToSprintForm,
    RemoveSprintForm,
    UpdateSprintForm,
)
from NearBeach.models import (
    ObjectAssignment,
    Project,
    RequirementItem,
    Sprint,
    Task,
    SprintObjectAssignment,
    UserGroup, Requirement
)
from NearBeach.views.gantt_chart_views import get_object_results
from NearBeach.views.theme_views import get_theme

from NearBeach.decorators.check_user_permissions.sprint_permissions import (
    check_sprint_permission_with_sprint,
    check_sprint_permissions_with_destination,
)

from NearBeach.decorators.check_user_permissions.object_permissions import check_user_generic_permissions

LOOKUP_FUNCS = {
    "project": {
        "object": Project.objects,
        "title": "project_name",
        "parent": "project",
    },
    "task": {
        "object": Task.objects,
        "title": "task_short_description",
        "parent": "task",
    },
    "requirement_item": {
        "object": RequirementItem.objects,
        "title": "requirement_item_title",
        "parent": "requirement",
    },
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

    object_results = get_object_results(location_id)

    results = {
        "gantt_chart_data": json.loads(object_results),
    }

    return JsonResponse(
        results,
        safe=False,
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def add_sprint_to_object(request, destination, location_id, sprint_id, *args, **kwargs):
    """
    User currently on an object information page. They have selected this object be added to an existing sprint.
    """
    form = NewSprintAssignmentForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    form_sprint = form.cleaned_data["sprint_id"]
    if not int(sprint_id) == form_sprint.sprint_id:
        return HttpResponseBadRequest("Mismatch sprint id")

    submit_sprint_assignment = SprintObjectAssignment(
        sprint_id=form_sprint,
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


@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def edit_sprint(request, sprint_id, *args, **kwargs):
    sprint_results = Sprint.objects.filter(
        is_deleted=False,
        sprint_id=sprint_id,
    )

    if sprint_results is None:
        return HttpResponseBadRequest("No sprints")

    sprint_start_date = sprint_results[0].sprint_start_date.isoformat()
    sprint_end_date = sprint_results[0].sprint_end_date.isoformat()

    t = loader.get_template("NearBeach/sprints/edit_sprint.html")

    c = {
        "need_tinymce": False,
        "sprint_end_date": sprint_end_date,
        "sprint_id": sprint_id,
        "sprint_name": sprint_results[0].sprint_name,
        "sprint_start_date": sprint_start_date,
        "sprint_status": sprint_results[0].sprint_status,
        "user_level": kwargs["user_level"],
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


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
@check_sprint_permission_with_sprint(min_permission_level=1)
def potential_object_list(request, destination, location_id, object_lookup, *args, **kwargs):
    """
    Used to get a list of potential objects that can be assigned to a sprint.
    """
    if not destination == "sprint":
        return HttpResponseBadRequest("Object has to be a sprint")

    if object_lookup not in LOOKUP_FUNCS:
        return HttpResponseBadRequest("Sorry - but that object lookup does not exist")

    # Get user groups
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
        group_id__isnull=False,
    ).values("group_id")

    # Depending on the object, we might need to look at the parent. If an object does not have
    # A parent, it will refer itself. i.e. project will refer project
    parent = LOOKUP_FUNCS[object_lookup]["parent"]
    object = LOOKUP_FUNCS[object_lookup]["object"]

    # Get both object exclusion and inclusion
    object_inclusion = ObjectAssignment.objects.filter(
        is_deleted=False,
        **{F"{parent}_id__isnull": False},
        group_id__in=user_group_results,
    ).exclude(
        **{F"{parent}__{parent}_status__{parent}_higher_order_status": "Closed"},
    ).values(
        F"{parent}_id"
    )

    # Get the data dependent on the object lookup
    data_results = object.filter(
        is_deleted=False,
        **{F"{parent}_id__in": object_inclusion}
    ).exclude(
        Q(
            **{F"{object_lookup}_status__{object_lookup}_higher_order_status": "Closed"},
        )
    ).annotate(
        id=F(F"{object_lookup}_id"),
        description=F(F"{LOOKUP_FUNCS[object_lookup]['title']}"),
        status=F(F"{object_lookup}_status__{object_lookup}_status")
    ).values(
        'id',
        'description',
        'status',
    )

    # If destination is requirement_item, we need to exclude any of it's
    # deleted parents
    if destination == "requirement_item":
        data_results = data_results.exclude(
            Q(
                requirement_id__in=Requirement.objects.filter(
                    is_deleted=True,
                ).values("requirement_id")
            )
            | Q(
                requirement_item_status__requirement_item_higher_order_status="Closed",
            )
        )

    # Exclude the data from data results
    data_results = data_results.filter().exclude(
        **{F"{object_lookup}_id__in": SprintObjectAssignment.objects.filter(
            sprint_id=location_id,
            **{F"{object_lookup}_id__isnull": False},
            is_deleted=False,
        ).values(
            F"{object_lookup}_id",
        )},
    )

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
def remove_sprint(request, destination, location_id, sprint_id, *args, **kwargs):
    form = RemoveSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    form_sprint = form.cleaned_data["sprint_id"]
    if not int(sprint_id) == form_sprint.sprint_id:
        return HttpResponseBadRequest("Mismatch sprint id")

    SprintObjectAssignment.objects.filter(
        **{F"{destination}_id": location_id},
        sprint_id=form_sprint,
    ).update(
        is_deleted=True,
    )

    sprint_results = get_assigned_sprints(destination, location_id)
    return JsonResponse(json.loads(sprint_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def remove_object_from_sprint(request, destination, location_id, *args, **kwargs):
    if not destination == "sprint":
        return HttpResponseBadRequest("Sorry - object not allowed")

    form = AddObjectToSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Soft delete the data
    for object_type in ["requirement_item", "project", "task"]:
        data = form.cleaned_data[object_type]

        # If there is data we'll have a set of one
        if len(data) == 1:
            SprintObjectAssignment.objects.filter(
                is_deleted=False,
                sprint_id=location_id,
                **{ F"{object_type}_id__in": data.values(F"{object_type}_id") }
            ).update(
                is_deleted=True,
            )

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(1)
def sprint_information(request, sprint_id, *args, **kwargs):
    # Get the template
    t = loader.get_template("NearBeach/sprints/sprint_information.html")

    sprint_results = Sprint.objects.filter(
        sprint_id=sprint_id,
        is_deleted=False,
    ).values(
        "sprint_id",
        "completed_story_points",
        "project",
        "requirement",
        "sprint_name",
        "sprint_end_date",
        "sprint_start_date",
        "sprint_status",
        "total_story_points",
    )

    if len(sprint_results) == 0:
        raise Http404

    gantt_start_date = sprint_results[0]['sprint_start_date'].isoformat()
    gantt_end_date = sprint_results[0]['sprint_end_date'].isoformat()

    c = {
        "gantt_end_date": gantt_end_date,
        "gantt_start_date": gantt_start_date,
        "sprint_status": sprint_results[0]['sprint_status'],
        "nearbeach_title": f"Sprint Information {sprint_id}",
        "need_tinymce": False,
        "sprint_id": sprint_id,
        "sprint_results": json.dumps(list(sprint_results), cls=DjangoJSONEncoder),
        "user_level": kwargs["user_level"],
        "theme": get_theme(request),
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


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_sprint_permission_with_sprint(2)
def update_sprint(request, sprint_id, *args, **kwargs):
    form = UpdateSprintForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_sprint = Sprint.objects.get(
        sprint_id=sprint_id,
    )

    update_sprint.sprint_name = form.cleaned_data["sprint_name"]
    update_sprint.sprint_status = form.cleaned_data["sprint_status"]
    update_sprint.sprint_start_date = form.cleaned_data["sprint_start_date"]
    update_sprint.sprint_end_date = form.cleaned_data["sprint_end_date"]

    update_sprint.save()

    return HttpResponse("")
