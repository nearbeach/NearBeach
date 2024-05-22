from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import ObjectAssignment, ScheduledObject, ObjectTemplate, UserGroup

import json


def new_scheduled_object(request):
    return HttpResponse("Setup view")


def new_scheduled_object_save(request):
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
        # object_template_type=F('object_template__object_template_type'),
        # object_template_json=F('object_template__object_template_json'),
    ).values(
        "schedule_object_id",
        "last_run",
        "next_scheduled_run",
        "is_active",
        "frequency",
        "frequency_attribute",
        # "object_template_id",
        # "object_template_type",
        # "object_template_json",
    )

    scheduled_object_results = json.dumps(list(scheduled_object_results), cls=DjangoJSONEncoder)

    # Context
    c = {
        "scheduled_object_results": json.loads(scheduled_object_results),
    }

    return HttpResponse(t.render(c, request))


def scheduled_object_information(request, scheduled_object_id):
    return HttpResponse("Setup view")