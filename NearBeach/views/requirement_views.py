import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F, Value as V
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import check_user_permissions
from NearBeach.forms import (
    AddRequirementLinkForm,
    NewRequirementForm,
    Organisation,
    UpdateRequirementForm,
)
from NearBeach.models import (
    Requirement,
    ObjectAssignment,
    Project,
    Task,
    RequirementItem,
    ListOfRequirementItemStatus,
    ListOfRequirementItemType,
    ListOfRequirementStatus,
    ListOfRequirementType,
    Group,
    UserGroup,
)
from NearBeach.views.theme_views import get_theme

import uuid


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=2, object_lookup="requirement_id")
def add_requirement_link(request, requirement_id, *args, **kwargs):
    """Check user form is valid"""
    form = AddRequirementLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the requirement instnace
    requirement_instance = Requirement.objects.get(requirement_id=requirement_id)

    # Get the project list from the form
    for row in request.POST.getlist("project"):
        submit_object_assignment = ObjectAssignment(
            requirement=requirement_instance,
            project=Project.objects.get(project_id=row),
            change_user=request.user,
            link_relationship="Relate"
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("task"):
        submit_object_assignment = ObjectAssignment(
            requirement=requirement_instance,
            task=Task.objects.get(task_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    return HttpResponse("Success")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="requirement_id")
def get_requirement_item_links(request, requirement_id, *args, **kwargs):
    # Get the object assignment results associated wtih that requirement
    object_assignment_results = ObjectAssignment.objects.filter(
        Q(
            is_deleted=False,
            requirement_item_id__in=RequirementItem.objects.filter(
                is_deleted=False,
                requirement_id=requirement_id,
            ).values("requirement_item_id"),
        )
    )


    # The results we want to send back
    data_results = []

    # Deal with the projects
    data_results.extend(object_assignment_results.filter(
        project_id__isnull=False,
    ).annotate(
        object_id=F("project_id"),
        object_title=F("project_id__project_name"),
        object_status=F("project_id__project_status__project_status"),
        object_type=V("project"),
    ).values(
        "object_id",
        "object_title",
        "object_status",
        "object_type",
        "requirement_item_id",
    ))

    data_results.extend(object_assignment_results.filter(
        task_id__isnull=False,
    ).annotate(
        object_id=F("task_id"),
        object_title=F("task_id__task_short_description"),
        object_status=F("task_id__task_status__task_status"),
        object_type=V("task"),
    ).values(
        "object_id",
        "object_title",
        "object_status",
        "object_type",
        "requirement_item_id",
    ))

    """
    As explained on stack overflow here -
    https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    return JsonResponse(data_results, safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="requirement_id")
def get_requirement_item_status_list(request, *args, **kwargs):
    """Get all status - even deleted ones."""
    status_list = ListOfRequirementItemStatus.objects.all()

    # Send back json data
    json_results = serializers.serialize("json", status_list)

    return HttpResponse(json_results, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="requirement_id")
def get_requirement_item_type_list(request, *args, **kwargs):
    """Get all status - even deleted ones."""
    type_list = ListOfRequirementItemType.objects.all()

    # Send back json data
    json_results = serializers.serialize("json", type_list)

    return HttpResponse(json_results, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="requirement_id")
def get_requirement_items(request, requirement_id, *args, **kwargs):
    """Get all the requirement items assigned to the requirement"""
    requirement_item_results = RequirementItem.objects.filter(
        is_deleted=False,
        requirement_id=requirement_id,
    ).annotate(
        requirement_item_status_text=F('requirement_item_status__requirement_item_status')
    ).values(
        'requirement_item_id',
        'requirement_item_title',
        'requirement_item_status_text',
    )

    # Send back json data
    json_results = json.dumps(list(requirement_item_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")




@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup="requirement_id")
def new_requirement(request, *args, **kwargs):
    """
    Loads the new requirement page
    :param request:
    :param location_id:
    :param destination:
    :return:
    """
    status_list = ListOfRequirementStatus.objects.filter(
        is_deleted=False,
    ).exclude(
        requirement_higher_order_status="Closed",
    )

    type_list = ListOfRequirementType.objects.filter(
        is_deleted=False,
    )

    group_results = Group.objects.filter(
        is_deleted=False,
    )

    # Get list of user groups
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

    # Load template
    t = loader.get_template("NearBeach/requirements/new_requirements.html")

    # context
    c = {
        "need_tinymce": True,
        "nearbeach_title": "New Requirements",
        "status_list": serializers.serialize("json", status_list),
        "type_list": serializers.serialize("json", type_list),
        "group_results": serializers.serialize("json", group_results),
        "user_group_results": json.dumps(
            list(user_group_results), cls=DjangoJSONEncoder
        ),
        "uuid": str(uuid.uuid4()),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup="requirement_id")
def new_requirement_save(request, *args, **kwargs):
    """Get the data and place into the form"""
    form = NewRequirementForm(request.POST)
    if not form.is_valid():
        # Something went wrong with the form.
        return HttpResponseBadRequest("There was something wrong with the form")

    # Save the form
    submit_requirement = Requirement(
        requirement_title=form.cleaned_data["requirement_title"],
        requirement_scope=form.cleaned_data["requirement_scope"],
        organisation=form.cleaned_data["organisation"],
        requirement_status=form.cleaned_data["requirement_status"],
        requirement_type=form.cleaned_data["requirement_type"],
        change_user=request.user,
        creation_user=request.user,
    )
    submit_requirement.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = Group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = ObjectAssignment(
            group_id=group_instance,
            requirement=submit_requirement,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(
        reverse("requirement_information", args={submit_requirement.requirement_id})
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="requirement_id")
def requirement_information(request, requirement_id, *args, **kwargs):
    """
    Loads the requirement information.
    :param request:
    :param requirement_id:
    :return:
    """
    user_level = kwargs["user_level"]

    # TODO: Check if I need to have a separate read only tempalte now.
    requirement_results = Requirement.objects.get(requirement_id=requirement_id)

    # Load template
    t = loader.get_template("NearBeach/requirements/requirement_information.html")

    # Get any extra data required
    organisation_results = Organisation.objects.get(
        organisation_id=requirement_results.organisation_id,
    )

    status_options = ListOfRequirementStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("requirement_status_id"),
        label=F("requirement_status"),
    ).values(
        "value",
        "label",
        "requirement_higher_order_status"
    ).order_by(
        "requirement_status_sort_order",
    )

    type_options = ListOfRequirementType.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("requirement_type_id"),
        label=F("requirement_type"),
    ).values(
        "value",
        "label",
    )

    group_results = Group.objects.filter(
        is_deleted=False,
    )

    requirement_item_results = RequirementItem.objects.filter(
        is_deleted=False,
        requirement_id=requirement_id,
    )

    # Check to see if the requirement is closed
    requirement_is_closed = requirement_results.requirement_status.requirement_higher_order_status == "Closed"
    if requirement_is_closed:
        requirement_is_closed = "true"
    else:
        requirement_is_closed = "false"

    # context
    c = {
        "group_results": serializers.serialize("json", group_results),
        "nearbeach_title": f"Requirement Information {requirement_id}",
        "need_tinymce": True,
        "organisation_results": serializers.serialize("json", [organisation_results]),
        "requirement_results": serializers.serialize("json", [requirement_results]),
        "requirement_id": requirement_id,
        "requirement_is_closed": requirement_is_closed,
        "requirement_item_results": serializers.serialize(
            "json", requirement_item_results
        ),
        "status_options": json.dumps(list(status_options), cls=DjangoJSONEncoder),
        "type_options": json.dumps(list(type_options), cls=DjangoJSONEncoder),
        "user_level": user_level,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=2, object_lookup="requirement_id")
def requirement_information_save(request, requirement_id, *args, **kwargs):
    """
    :param request:
    :param requirement_id:
    :return:
    """
    form = UpdateRequirementForm(request.POST)

    # If there is an error - notify the user
    if not form.is_valid():
        return HttpResponseBadRequest(
            f"Sorry, there is an error with the form: {form.errors}"
        )

    # Get the requirement
    requirement_result = Requirement.objects.get(requirement_id=requirement_id)

    # Update all the fields
    requirement_result.requirement_title = form.cleaned_data["requirement_title"]
    requirement_result.requirement_scope = form.cleaned_data["requirement_scope"]
    requirement_result.requirement_status = form.cleaned_data["requirement_status"]
    requirement_result.requirement_type = form.cleaned_data["requirement_type"]

    requirement_result.save()

    # Return a success
    return HttpResponse("Requirement Saved")
