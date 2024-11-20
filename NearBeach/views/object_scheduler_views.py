from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
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
from NearBeach.views.tools.internal_functions import lookup_choice_from_key, get_all_groups, get_user_group_permission
from NearBeach.forms import NewScheduledObjectForm, ScheduledObjectForm
from NearBeach.models import OBJECT_TEMPLATE_TYPE

import json
import uuid


def get_frequency_attribute(scheduler_frequency, form):
    if scheduler_frequency == "Set Day of the Week":
        json_frequency_attribute = json.dumps(
            {
                "days_of_the_week": form.cleaned_data["day"],
            },
            cls=DjangoJSONEncoder,
        )
        return json.loads(json_frequency_attribute)
    elif scheduler_frequency in ("Weekly", "Fortnightly"):
        json_frequency_attribute = json.dumps(
            {
                "day_of_the_week": form.cleaned_data["single_day"],
            },
            cls=DjangoJSONEncoder,
        )
        return json.loads(json_frequency_attribute)
    elif form.cleaned_data["scheduler_frequency"] == "X Days before End of the Month":
        json_frequency_attribute = json.dumps(
            {
                "days_before": form.cleaned_data["days_before"],
            },
            cls=DjangoJSONEncoder,
        )
        return json.loads(json_frequency_attribute)

    return json.loads("{}")


def new_scheduled_object(request):
    """
    New Scheduled Object
    ~~~~~~~~~~~~~~~~~~~~
    Renders the template for creating a new scheduled object.
    """
    t = loader.get_template("NearBeach/object_scheduler/new_scheduled_object.html")

    c = {
        "group_results": get_all_groups(),
        "need_tinymce": True,
        "nearbeach_title": "New Scheduled Object",
        "theme": get_theme(request),
        "user_group_permissions": get_user_group_permission(request.user, ["project"]),
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
        "object_organisation": organisation.organisation_id,
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
        frequency_attribute=get_frequency_attribute(scheduler_frequency, form),
    )

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
        organisation_id=object_template_results[0]["object_template_json"]["object_organisation"],
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


@login_required(login_url="login", redirect_field_name="")
def scheduled_object_information_save(request, schedule_object_id, *args, **kwargs):
    form = ScheduledObjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the object template and scheduled object
    update_scheduled_object = ScheduledObject.objects.get(schedule_object_id=schedule_object_id)
    update_object_template = update_scheduled_object.object_template

    # Update the object template
    organisation_information = Organisation.objects.get(
        organisation_id=update_object_template.object_template_json["object_organisation"],
    )

    object_json = json.dumps({
        "object_type": lookup_choice_from_key(
            OBJECT_TEMPLATE_TYPE,
            int(form.cleaned_data["object_type"]),
        ),
        "object_title": form.cleaned_data["object_title"],
        "object_description": form.cleaned_data["object_description"],
        "object_organisation": organisation_information.organisation_id,
        "object_start_date": form.cleaned_data["object_start_date"],
        "object_end_date": form.cleaned_data["object_end_date"],
        "uuid": update_object_template.object_template_json["uuid"],
        # "group_list": group_list,
    }, cls=DjangoJSONEncoder)

    update_object_template.object_template_type = form.cleaned_data["object_type"]
    update_object_template.object_template_json = json.loads(object_json)
    update_object_template.change_user = request.user
    update_object_template.save()

    # Delete all group connections
    # LOOK AT REMOVING THE DELETE FUNCTIONALITY, AND APPLYING A SOFT UPDATE
    ObjectTemplateGroup.objects.filter(
        is_deleted=False,
        object_template=update_object_template,
    ).delete()

    # Re-add in all group connections
    # Save all groups against the tempalte
    for group in form.cleaned_data["group_list"]:
        submit_object_template_group = ObjectTemplateGroup(
            group=group,
            object_template=update_object_template,
            change_user=request.user,
        )
        submit_object_template_group.save()

    # Grab the scheduler frequency
    scheduler_frequency = form.cleaned_data["scheduler_frequency"]

    # Update the scheduler Object
    update_scheduled_object.schedule_object_title=form.cleaned_data['object_title']
    update_scheduled_object.change_user=request.user
    update_scheduled_object.frequency=scheduler_frequency
    update_scheduled_object.start_date=form.cleaned_data["scheduler_start_date"]
    update_scheduled_object.frequency_attribute=get_frequency_attribute(scheduler_frequency, form)
    update_scheduled_object.is_active=form.cleaned_data["is_active"]

    # Handle number of repeats - default values first then add
    update_scheduled_object.number_of_repeats = -1
    update_scheduled_object.end_date = None
    if form.cleaned_data["end_date_condition"] == "number-of-repeats":
        update_scheduled_object.number_of_repeats = form.cleaned_data["number_of_repeats"]
    elif form.cleaned_data["end_date_condition"] == "end-date":
        update_scheduled_object.end_date = form.cleaned_data["scheduler_end_date"]

    update_scheduled_object.save()

    return HttpResponse()
