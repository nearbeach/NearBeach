from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods

from NearBeach.forms import ObjectStatusReorderForm, ObjectStatusCreateForm, ObjectStatusUpdateForm, \
    ObjectStatusDeleteForm
from NearBeach.views.theme_views import get_theme
from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfRequirementStatus,
    ListOfProjectStatus,
    ListOfTaskStatus,
    RequirementItem,
    Requirement,
    Project,
    Task,
)

import json

OBJECT_LOOKUP = {
    "requirement_item": ListOfRequirementItemStatus,
    "requirement": ListOfRequirementStatus,
    "project": ListOfProjectStatus,
    "task": ListOfTaskStatus,
}

OBJECT_OBJECT_LOOKUP = {
    "requirement_item": RequirementItem,
    "requirement": Requirement,
    "project": Project,
    "task": Task,
}

OBJECT_NAME_LOOKUP = {
   "requirement_item": "Requirement Item",
   "requirement": "Requirement",
   "project": "Project",
   "task": "Task",
}


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def object_status_create(request, destination):
    form = ObjectStatusCreateForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the length of the object
    sort_order = len(OBJECT_LOOKUP[destination].objects.filter(
        is_deleted=False,
    ))

    object_submit = OBJECT_LOOKUP[destination]()
    setattr(
        object_submit,
        F"{destination}_status",
        form.cleaned_data["status"],
    )
    setattr(
        object_submit,
        F"{destination}_higher_order_status",
        form.cleaned_data["higher_order_status"]
    )
    setattr(
        object_submit,
        F"{destination}_status_sort_order",
        sort_order
    )

    object_submit.save()

    # Send back the data object
    object_status_results = OBJECT_LOOKUP[destination].objects.filter(
        **{F"{destination}_status_id": getattr(object_submit, F"{destination}_status_id")},
    ).annotate(
        higher_order_status=F(F"{destination}_higher_order_status"),
        status_id=F(F"{destination}_status_id"),
        status=F(F"{destination}_status"),
        status_sort_order=F(F"{destination}_status_sort_order"),
    ).values(
        "higher_order_status",
        "status_id",
        "status",
        "status_sort_order",
    )

    data_results = json.dumps(list(object_status_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(data_results), safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def object_status_delete(request, destination):
    form = ObjectStatusDeleteForm(request.POST, destination=destination)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get data from form
    status_object = form.cleaned_data["status_id"]
    migration_status_object = form.cleaned_data["migration_status_id"]

    # Soft delete the status :)
    OBJECT_LOOKUP[destination].objects.filter(
        **{F"{destination}_status_id": getattr(status_object, F"{destination}_status_id")},
    ).update(
        is_deleted=True,
    )

    # Migrate all objects that have that status to the new status
    OBJECT_OBJECT_LOOKUP[destination].objects.filter(
        **{F"{destination}_status_id": getattr(status_object, F"{destination}_status_id")},
    ).update(
        **{F"{destination}_status_id": getattr(migration_status_object, F"{destination}_status_id")}
    )

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def object_status_information(request, destination):
    t = loader.get_template("./NearBeach/object_status/object_status_information.html")

    object_status_results = OBJECT_LOOKUP[destination].objects.filter(
        is_deleted=False,
    ).order_by(
        F"{destination}_status_sort_order"
    ).annotate(
        higher_order_status=F(F"{destination}_higher_order_status"),
        status_id=F(F"{destination}_status_id"),
        status=F(F"{destination}_status"),
        status_sort_order=F(F"{destination}_status_sort_order"),
    ).values(
        "higher_order_status",
        "status_id",
        "status",
        "status_sort_order",
    )

    c = {
        "destination": destination,
        "nearbeach_title": F"{OBJECT_NAME_LOOKUP[destination]} Status Editor",
        "need_tinymce": False,
        "object_status_results": json.dumps(list(object_status_results), cls=DjangoJSONEncoder),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def object_status_list(request):
    t = loader.get_template("./NearBeach/object_status/object_status_list.html")

    c = {
        "nearbeach_title": "Object Status List",
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def object_status_reorder(request, destination):
    form = ObjectStatusReorderForm(request.POST, destination=destination)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extra the data
    status_id_list = request.POST.getlist("status_id")

    # Look through the status id list and re-index the order
    for index, item in enumerate(status_id_list, start=0):
        # Filter for the specific table and field names
        status_update = OBJECT_LOOKUP[destination].objects.get(
            **{F"{destination}_status_id": item}
        )

        setattr(
            status_update,
            F"{destination}_status_sort_order",
            index
        )
        status_update.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def object_status_update(request, destination):
    form = ObjectStatusUpdateForm(request.POST, destination=destination)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the status object
    status_object = form.cleaned_data["status_id"]

    # Create the ORM to update the status
    status_update = OBJECT_LOOKUP[destination].objects.get(
        **{F"{destination}_status_id": getattr(status_object, F"{destination}_status_id")}
    )
    setattr(
        status_update,
        F"{destination}_status",
        form.cleaned_data["status"],
    )
    setattr(
        status_update,
        F"{destination}_higher_order_status",
        form.cleaned_data["higher_order_status"]
    )

    status_update.save()

    return HttpResponse("")
