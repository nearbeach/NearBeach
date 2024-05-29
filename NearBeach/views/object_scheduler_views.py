from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.db.models import F, Max
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import ObjectAssignment, ScheduledObject, ObjectTemplate, UserGroup, Group
from NearBeach.views.theme_views import get_theme
from NearBeach.views.tools.internal_functions import lookup_choice_from_key
from NearBeach.forms import NewScheduledObjectForm
from NearBeach.models import OBJECT_TEMPLATE_TYPE

import json
import uuid


def new_scheduled_object(request):
    """
    New Scheduled Object
    ~~~~~~~~~~~~~~~~~~~~
    Renders the template for creating a new scheduled object.
    """
    t = loader.get_template("NearBeach/object_scheduler/new_scheduled_object.html")

    # Get the data
    group_results = Group.objects.filter(
        is_deleted=False,
    )

    # User group and level results
    user_group_and_level = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    ).values(
        "group_id",
        "group__group_name",
    ).annotate(
        project_permission=Max("permission_set__project"),
    ).annotate(
        task_permission=Max("permission_set__task"),
    )

    # Get the USER groups
    user_group_results = (
        UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        )
        .values(
            "group_id",
            "group__group_name",
        )
        .distinct()
    )

    c = {
        "group_results": serializers.serialize("json", group_results),
        "need_tinymce": True,
        "nearbeach_title": "New Scheduled Object",
        "theme": get_theme(request),
        "user_group_and_level": json.dumps(
            list(user_group_and_level),
            cls=DjangoJSONEncoder,
        ),
        "user_group_results": json.dumps(
            list(user_group_results),
            cls=DjangoJSONEncoder
        ),
        "uuid": str(uuid.uuid4()),
    }

    return HttpResponse(t.render(c, request))


def new_scheduled_object_save(request):
    form = NewScheduledObjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Prepare the group list
    group_list = []
    for group in form.cleaned_data["group_list"]:
        group_list.append(
            group.group_id,
        )

    # Setup the object_json
    organisation = form.cleaned_data["organisation"]
    object_json = json.dumps({
        "object_type": lookup_choice_from_key(
            OBJECT_TEMPLATE_TYPE,
            int(form.cleaned_data["object_type"]),
        ),
        "object_title": form.cleaned_data["object_title"],
        "object_description": form.cleaned_data["object_description"],
        "organisation": organisation.organisation_id,
        "object_start_date": form.cleaned_data["object_start_date"],
        "object_end_date": form.cleaned_data["object_end_date"],
        "uuid": form.cleaned_data["uuid"],
        "group_list": group_list,
    }, cls=DjangoJSONEncoder)

    # Save data
    submit_object_template = ObjectTemplate(
        object_template_type=form.cleaned_data["object_type"],
        object_template_json=json.loads(object_json),
        change_user=request.user,
    )
    submit_object_template.save()

    return HttpResponse("Setup view")


def scheduled_objects(request):
    """
    Scheduled Objects
    ~~~~~~~~~~~~~~~~~
    Loads up a list of objects for the user
    """
    t = loader.get_template("NearBeach/object_scheduler/scheduled_objects.html")

    # Grab all object assignments for the object template
    object_assignments = ObjectAssignment.objects.filter(
        is_deleted=False,
        object_template__isnull=False,
        group_id__in=UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        ).values("group_id")
    )

    # Grab the scheduled objects that the user has access too
    scheduled_object_results = ScheduledObject.objects.filter(
        is_deleted=False,
        object_template__in=object_assignments.values("object_template_id"),
    ).annotate(
        object_template_type=F('object_template__object_template_type'),
        object_template_json=F('object_template__object_template_json'),
    ).values(
        "schedule_object_id",
        "last_run",
        "next_scheduled_run",
        "is_active",
        "frequency",
        "frequency_attribute",
        "object_template_id",
        "object_template_type",
        "object_template_json",
    )

    scheduled_object_results = json.dumps(list(scheduled_object_results), cls=DjangoJSONEncoder)

    # User Level
    # Get the max user levels from the user group table
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    ).aggregate(
        Max("permission_set__project"),
        Max("permission_set__task"),
    )

    # Place these max values within the data
    user_level = json.dumps(
        {
            "project": user_group_results["permission_set__project__max"],
            "task": user_group_results["permission_set__task__max"],
        },
        cls=DjangoJSONEncoder,
    )

    # Context
    c = {
        "nearbeach_title": "Scheduled Objects",
        "scheduled_object_results": json.loads(scheduled_object_results),
        "theme": get_theme(request),
        "user_level": json.loads(user_level),
    }

    return HttpResponse(t.render(c, request))


def scheduled_object_information(request, scheduled_object_id):
    return HttpResponse("Setup view")