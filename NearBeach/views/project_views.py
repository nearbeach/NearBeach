from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.template import loader
from NearBeach.forms import NewProjectForm, ProjectForm
from NearBeach.models import Group, UserGroup, ObjectAssignment, ListOfProjectStatus
from NearBeach.views.tools.internal_functions import Project, Organisation
from NearBeach.decorators.check_user_permissions import check_user_permissions
from NearBeach.views.theme_views import get_theme
from NearBeach.views.document_views import transfer_new_object_uploads

import json, uuid


@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup="project_id")
def new_project(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    t = loader.get_template("NearBeach/projects/new_project.html")

    # Get data we require
    group_results = Group.objects.filter(
        is_deleted=False,
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

    user_level = kwargs["user_level"]

    # Context
    c = {
        "group_results": serializers.serialize("json", group_results),
        "need_tinymce": True,
        "nearbeach_title": "New Project",
        "theme": get_theme(request),
        "user_group_results": json.dumps(
            list(user_group_results), cls=DjangoJSONEncoder
        ),
        "user_level": user_level,
        "uuid": str(uuid.uuid4()),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup="project_id")
def new_project_save(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Get the form data
    form = NewProjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get first project status
    project_status = ListOfProjectStatus.objects.filter(
        is_deleted=False
    ).order_by(
        "project_status_order",
    )

    if len(project_status) == 0:
        return HttpResponseBadRequest("No Project Status entered in the system. Please contact system admin")

    # Create the project
    project_submit = Project(
        change_user=request.user,
        creation_user=request.user,
        project_name=form.cleaned_data["project_name"],
        project_description=form.cleaned_data["project_description"],
        project_start_date=form.cleaned_data["project_start_date"],
        project_end_date=form.cleaned_data["project_end_date"],
        organisation=form.cleaned_data["organisation"],
        project_status=project_status.first(),
    )
    project_submit.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = Group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = ObjectAssignment(
            group_id=group_instance,
            project=project_submit,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Transfer any images to the new project id
    transfer_new_object_uploads("project", project_submit.project_id, form.cleaned_data['uuid'])

    # Send back requirement_information URL
    return HttpResponse(
        reverse("project_information", args={project_submit.project_id})
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="project_id")
def project_information(request, project_id, *args, **kwargs):
    """
    :param request:
    :param project_id:
    :return:
    """
    # Template
    t = loader.get_template("NearBeach/projects/project_information.html")

    # Get data
    project_results = Project.objects.get(project_id=project_id)
    user_level = kwargs["user_level"]
    project_is_closed = project_results.project_status.project_higher_order_status == "Closed"

    # Grab all the status options for the project. Shape the data into the required shape for frontend
    status_options = ListOfProjectStatus.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F('project_status_id'),
        label=F('project_status'),
    ).values(
        "value",
        "label",
        "project_higher_order_status",
    ).order_by(
        "project_status_order"
    )

    # Get the organisation results
    organisation_results = Organisation.objects.filter(
        is_deleted=False,
        organisation_id=project_results.organisation_id,
    )

    # Update user level if currently read only - and convert project_is_closed to JS boolean
    if project_is_closed:
        project_is_closed = "true"
    else:
        project_is_closed = "false"

    # Context
    c = {
        "nearbeach_title": f"Project Information {project_id}",
        "need_tinymce": True,
        "organisation_results": serializers.serialize("json", organisation_results),
        "project_id": project_id,
        "project_is_closed": project_is_closed,
        "project_results": serializers.serialize("json", [project_results]),
        "status_options": json.dumps(list(status_options), cls=DjangoJSONEncoder),
        "user_level": user_level,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=2, object_lookup="project_id")
def project_information_save(request, project_id, *args, **kwargs):
    """
    :param request:
    :param project_id:
    :return:
    """
    # Get the form data
    form = ProjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the project data
    project_update = Project.objects.get(project_id=project_id)
    project_update.project_name = form.cleaned_data["project_name"]
    project_update.project_description = form.cleaned_data["project_description"]
    project_update.project_start_date = form.cleaned_data["project_start_date"]
    project_update.project_end_date = form.cleaned_data["project_end_date"]
    project_update.project_status = form.cleaned_data["project_status"]

    # Save
    project_update.save()

    return HttpResponse("Good")
