import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import (
    check_user_requirement_item_permissions,
    check_user_permissions,
)
from NearBeach.forms import (
    AddRequirementLinkForm,
    NewRequirementItemForm,
    UpdateRequirementItemForm,
)
from NearBeach.views.requirement_views import get_requirement_items
from NearBeach.models import (
    RequirementItem,
    ObjectAssignment,
    Project,
    Task,
    Requirement,
    Organisation,
    ListOfRequirementItemStatus,
    ListOfRequirementItemType,
    Group,
)
from NearBeach.views.theme_views import get_theme


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_requirement_item_permissions(min_permission_level=2)
def add_requirement_item_link(request, requirement_item_id, *args, **kwargs):
    """Obtain form data and validate"""
    form = AddRequirementLinkForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the requirement instnace
    requirement_item_instance = RequirementItem.objects.get(
        requirement_item_id=requirement_item_id
    )

    # Get the project list from the form
    for row in request.POST.getlist("project"):
        submit_object_assignment = ObjectAssignment(
            requirement_item=requirement_item_instance,
            project=Project.objects.get(project_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("task"):
        submit_object_assignment = ObjectAssignment(
            requirement_item=requirement_item_instance,
            task=Task.objects.get(task_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    # Now return back a complete list of new links
    link_results = get_requirement_item_links(requirement_item_id)

    # Send back json data
    json_results = json.dumps(list(link_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


# Internal Code
def get_requirement_item_links(requirement_item_id):
    """Use object_assignment to get the requirments"""
    return ObjectAssignment.objects.filter(
        Q(is_deleted=False, requirement_item_id=requirement_item_id)
        & Q(Q(project_id__isnull=False) | Q(task_id__isnull=False))
    ).values(
        "project_id",
        "project_id__project_name",
        "project_id__project_status",
        "task_id",
        "task_id__task_short_description",
        "task_id__task_status",
        "requirement_item_id",
        "requirement_item_id__requirement_item_title",
    )




@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup="requirement_id")
def new_requirement_item(request, requirement_id, *args, **kwargs):
    """Check to see if POST"""
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - needs to be in POST")

    # Get the data into the form for cleaning
    form = NewRequirementItemForm(request.POST)

    # Check to make sure there are no errors in the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_requirement_item = RequirementItem(
        requirement=Requirement.objects.get(requirement_id=requirement_id),
        requirement_item_title=form.cleaned_data["requirement_item_title"],
        requirement_item_scope=form.cleaned_data["requirement_item_scope"],
        requirement_item_status=form.cleaned_data["requirement_item_status"],
        requirement_item_type=form.cleaned_data["requirement_item_type"],
        change_user=request.user,
    )
    submit_requirement_item.save()

    # Actuall return all the new requirement_item results to feed upstream
    return get_requirement_items(request, requirement_id)


@login_required(login_url="login", redirect_field_name="")
@check_user_requirement_item_permissions(min_permission_level=1)
def requirement_item_information(request, requirement_item_id, *args, **kwargs):
    """
    Loads the requirement item information.
    :param request:
    :param requirement_item_id:
    :return:
    """
    user_level = kwargs["user_level"]

    # Get the requirement information
    requirement_item_results = RequirementItem.objects.get(
        requirement_item_id=requirement_item_id
    )

    # If the requirement has been closed - send user to the read only section
    if requirement_item_results.requirement_item_status.status_is_closed:
        return HttpResponseRedirect(
            reverse("requirement_readonly", args={requirement_item_id})
        )

    # Load template
    t = loader.get_template(
        "NearBeach/requirement_items/requirement_item_information.html"
    )

    # Get any extra data required
    organisation_results = Organisation.objects.get(
        organisation_id=requirement_item_results.requirement.organisation_id,
    )

    status_list = ListOfRequirementItemStatus.objects.filter(
        is_deleted=False,
        status_is_closed=False,
    )

    type_list = ListOfRequirementItemType.objects.filter(
        is_deleted=False,
    )

    group_results = Group.objects.filter(
        is_deleted=False,
    )

    # context
    c = {
        "group_results": serializers.serialize("json", group_results),
        "nearbeach_title": f"Requirement Item {requirement_item_id}",
        "organisation_results": serializers.serialize("json", [organisation_results]),
        "requirement_item_id": requirement_item_id,
        "requirement_item_results": serializers.serialize(
            "json", [requirement_item_results]
        ),
        "status_list": serializers.serialize("json", status_list),
        "type_list": serializers.serialize("json", type_list),
        "user_level": user_level,
        "need_tinymce": True,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_requirement_item_permissions(min_permission_level=2)
def requirement_information_save(request, requirement_item_id, *args, **kwargs):
    """
    The following will save data
    :param request:
    :param requirement_id:
    :return:
    """
    # Get form data
    form = UpdateRequirementItemForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    requirement_item_submit = RequirementItem.objects.get(
        requirement_item_id=requirement_item_id
    )
    requirement_item_submit.change_user = request.user
    requirement_item_submit.requirement_item_title = form.cleaned_data[
        "requirement_item_title"
    ]
    requirement_item_submit.requirement_item_scope = form.cleaned_data[
        "requirement_item_scope"
    ]
    requirement_item_submit.requirement_item_status = form.cleaned_data[
        "requirement_item_status"
    ]
    requirement_item_submit.requirement_item_type = form.cleaned_data[
        "requirement_item_type"
    ]
    requirement_item_submit.save()

    # Send back an empty response
    return HttpResponse("")
