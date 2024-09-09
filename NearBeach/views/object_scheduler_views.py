from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.db.models import F, Max
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import (
    Group,
    ObjectTemplate,
    ObjectTemplateGroup,
    Organisation,
    ScheduledObject,
    UserGroup,
)
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
        # "group_list": group_list,
    }, cls=DjangoJSONEncoder)

    # Save data
    submit_object_template = ObjectTemplate(
        object_template_type=form.cleaned_data["object_type"],
        object_template_json=json.loads(object_json),
        change_user=request.user,
    )
    submit_object_template.save()

    # Save all groups against the tempalte
    for group in form.cleaned_data["group_list"]:
        submit_object_template_group = ObjectTemplateGroup(
            group=group,
            object_template=submit_object_template,
            change_user=request.user,
        )
        submit_object_template_group.save()

    # Create the scheduled object
    scheduler_frequency = form.cleaned_data["scheduler_frequency"]

    submit_scheduled_object = ScheduledObject(
        schedule_object_title=form.cleaned_data['object_title'],
        change_user=request.user,
        frequency=scheduler_frequency,
        start_date=form.cleaned_data["scheduler_start_date"],
        object_template=submit_object_template,
    )

    if scheduler_frequency == "Set Day of the Week":
        json_frequency_attribute = json.dumps(
            {
                "days_of_the_week": form.cleaned_data["day"],
            },
            cls=DjangoJSONEncoder,
        )
        submit_scheduled_object.frequency_attribute = json.loads(json_frequency_attribute)
    elif scheduler_frequency == "Weekly" or scheduler_frequency == "Fortnightly":
        json_frequency_attribute = json.dumps(
            {
                "day_of_the_week": form.cleaned_data["single_day"],
            },
            cls=DjangoJSONEncoder,
        )
        submit_scheduled_object.frequency_attribute = json.loads(json_frequency_attribute)

    elif form.cleaned_data["scheduler_frequency"] == "X Days before End of the Month":
        json_frequency_attribute = json.dumps(
            {
                "days_before": form.cleaned_data["days_before"],
            },
            cls=DjangoJSONEncoder,
        )
        submit_scheduled_object.frequency_attribute = json.loads(json_frequency_attribute)

    # Handle number of repeats
    if form.cleaned_data["end_date_condition"] == "number-of-repeats":
        submit_scheduled_object.number_of_repeats = form.cleaned_data["number_of_repeats"]
    elif form.cleaned_data["end_date_condition"] == "end-date":
        submit_scheduled_object.end_date = form.cleaned_data["scheduler_end_date"]

    # Save
    submit_scheduled_object.save()

    return JsonResponse(
        {
            "scheduled_object_id": submit_scheduled_object.schedule_object_id,
        },
        safe=True
    )


def scheduled_objects(request):
    """
    Scheduled Objects
    ~~~~~~~~~~~~~~~~~
    Loads up a list of objects for the user
    """
    t = loader.get_template("NearBeach/object_scheduler/scheduled_objects.html")

    # Grab all object assignments for the object template
    # object_assignments = ObjectAssignment.objects.filter(
    #     is_deleted=False,
    #     object_template__isnull=False,
    #     group_id__in=UserGroup.objects.filter(
    #         is_deleted=False,
    #         username=request.user,
    #     ).values("group_id")
    # )
    object_template_group_results = ObjectTemplateGroup.objects.filter(
        is_deleted=False,
        group_id__in=UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        ).values("group_id"),
    )

    # Grab the scheduled objects that the user has access too
    scheduled_object_results = ScheduledObject.objects.filter(
        is_deleted=False,
        object_template__in=object_template_group_results.values("object_template_id"),
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


@login_required(login_url="login", redirect_field_name="")
def scheduled_object_information(request, schedule_object_id, *args, **kwargs):
    # Template
    t = loader.get_template("NearBeach/object_scheduler/scheduled_object_information.html")

    # Get data
    scheduled_object_results = ScheduledObject.objects.filter(
        schedule_object_id=schedule_object_id
    ).values(
        "schedule_object_id",
        "object_template_id",
        "end_date",
        "start_date",
        "frequency",
        "frequency_attribute",
        "is_active",
        "number_of_repeats",
    )

    # Check to make sure there is a scheduled object results
    if len(scheduled_object_results) == 0:
        return HttpResponseBadRequest("Sorry, no object")

    scheduled_object_results = scheduled_object_results.first()

    object_template_results = ObjectTemplate.objects.filter(
        object_template_id=scheduled_object_results["object_template_id"]
    ).values(
        'object_template_json',
        'object_template_type',
    )

    organisation_information = Organisation.objects.get(
        organisation_id=object_template_results[0]["object_template_json"]["organisation"],
    )

    group_results = Group.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("group_id"),
        label=F("group_name"),
    ).values(
        "value",
        "label",
    )

    template_group_results = ObjectTemplateGroup.objects.filter(
        object_template_id=scheduled_object_results["object_template_id"],
        is_deleted=False,
    ).values(
        "group_id",
    ).values_list(
        'group_id',
        flat=True
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
        ).distinct()
    )

    group_results = json.dumps(list(group_results), cls=DjangoJSONEncoder)
    object_template_results = json.dumps(list(object_template_results), cls=DjangoJSONEncoder)
    template_group_results = json.dumps(list(template_group_results), cls=DjangoJSONEncoder)
    scheduled_object_results = json.dumps(scheduled_object_results, cls=DjangoJSONEncoder)

    c = {
        "group_results": group_results,
        "nearbeach_title": f"Scheduled Object {schedule_object_id}",
        "need_tinymce": True,
        "object_template_results": object_template_results,
        "organisation_results": serializers.serialize("json", [organisation_information]),
        "scheduled_object_id": schedule_object_id,
        "scheduled_object_results": scheduled_object_results,
        "template_group_results": template_group_results,
        "user_group_and_level": json.dumps(
            list(user_group_and_level),
            cls=DjangoJSONEncoder,
        ),
        "user_group_results": json.dumps(
            list(user_group_results),
            cls=DjangoJSONEncoder
        ),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))
