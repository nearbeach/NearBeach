import json
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, F
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from NearBeach.views.search.search_objects import SearchObjects
from NearBeach.forms import SearchObjectsForm, SearchForm
from NearBeach.models import (
    Notification,
    ObjectAssignment,
    Customer,
    Group,
    Organisation,
    PermissionSet,
    Sprint,
    User,
    Tag,
    UserGroup, ObjectTemplateGroup, ScheduledObject,
)
from NearBeach.views.theme_views import get_theme
from NearBeach.decorators.check_user_permissions.admin_permissions import check_user_admin_permissions
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions

import math

# Define global variables
SEARCH_PAGE_SIZE = getattr(settings, 'SEARCH_PAGE_SIZE', 5)


# Internal Function
def get_sprint_search_data(search_form, request):
    object_assignment_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        group_id__in=UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        ).values('group_id'),
    )

    # Gather the sprint results
    sprint_results = Sprint.objects.filter(
        Q(
            is_deleted=False,
        ) &
        Q(
            Q(
                requirement_id__in=object_assignment_results.values('requirement_id'),
            ) |
            Q(
                project_id__in=object_assignment_results.values('project_id'),
            )
        )
    )

    # Only include opened/current results
    if not search_form.cleaned_data["include_closed"]:
        sprint_results = sprint_results.exclude(
            sprint_status="Finished"
        )

    # Check to see if we are filtering any names
    for split_row in search_form.cleaned_data["search"].split(" "):
        sprint_results = sprint_results.filter(
            Q(sprint_name__icontains=split_row)
        )

    sprint_results = sprint_results.values(
        "sprint_id",
        "sprint_name",
        "sprint_status",
    )

    # Pagination :D
    destination_page = search_form.cleaned_data["destination_page"]

    # Apply the shift of the destination page, as we should -1 the value. Due to the front end sending the actual
    # page number
    destination_page = 0 if destination_page <= 0 else destination_page - 1

    return sprint_results[destination_page * SEARCH_PAGE_SIZE:(destination_page + 1) * SEARCH_PAGE_SIZE], len(sprint_results)


@login_required(login_url="login", redirect_field_name="")
def search(request):
    """
    :param request:
    :return:
    """
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Template
    t = loader.get_template("NearBeach/search/search.html")

    # Translate the is_superuser, from Python Boolean to JavaScript boolean
    if request.user.is_superuser:
        is_superuser = "true"
    else:
        is_superuser = "false"

    # Context
    c = {
        "is_superuser": is_superuser,
        "need_tinymce": False,
        "nearbeach_title": "Search",
        "search_input": form.cleaned_data["search"],
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_data(request):
    """
    :param request:
    :return:
    """
    # Get the form data
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    search_results = SearchObjects(form, request)

    # Return the JSON data
    return JsonResponse(search_results.results)


@login_required(login_url="login", redirect_field_name="")
def search_customer(request):
    """
    :param request:
    :return:
    """
    t = loader.get_template("NearBeach/search/search_customers.html")

    # Get the first 50 customers
    customer_results = Customer.objects.filter(is_deleted=False,).order_by(
        "customer_last_name", "customer_first_name"
    )[:50]

    c = {
        "need_tinymce": False,
        "customer_results": serializers.serialize("json", customer_results),
        "nearbeach_title": "Search Customers",
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_customer_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    customer_results = Customer.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data["search"].split(" "):
        # Update the organisation results SQL
        customer_results = customer_results.filter(
            Q(customer_first_name__icontains=split_row)
            | Q(customer_last_name__icontains=split_row)
            |
            # Might not work for freelancers
            Q(organisation__organisation_name__icontains=split_row)
        )

    # Only have 50 results and order by alphabetical order
    customer_results = customer_results.order_by(
        "customer_last_name", "customer_first_name"
    )[:50]

    # Send back json data
    json_results = serializers.serialize("json", customer_results)

    return HttpResponse(json_results, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def search_group(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # ADD IN PERMISSIONS
    # Get template
    t = loader.get_template("NearBeach/search/search_groups.html")

    # Get user data
    group_results = Group.objects.filter(is_deleted=False,).order_by(
        "group_name"
    )[:25]

    # Get context
    c = {
        "group_results": serializers.serialize("json", group_results),
        "nearbeach_title": "Search Groups",
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
def search_group_data(request):
    """
    :param request:
    :return:
    """
    # Obtain form data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # Get the base group results
    group_results = Group.objects.filter(
        is_deleted=False,
    )

    # Loop through the search results
    for split_row in search_form.cleaned_data["search"].split(" "):
        group_results = group_results.filter(
            group_name__icontains=split_row,
        )

    group_results = group_results.order_by("group_name")[:25]

    # Send back json data
    json_results = serializers.serialize("json", group_results)

    return HttpResponse(json_results, content_type="application/json")


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def search_notification(request):
    t = loader.get_template("NearBeach/search/search_notifications.html")

    notification_results = Notification.objects.filter(
        is_deleted=False
    )

    c = {
        "need_tinymce": False,
        "nearbeach_title": "Search Notifications",
        "notification_results": serializers.serialize("json", notification_results),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_notification_data(request):
    """
    :param request:
    :return:
    """
    # Obtain form data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # Get the base group results
    notification_results = Notification.objects.filter(
        is_deleted=False
    )

    # Loop through the search results
    for split_row in search_form.cleaned_data["search"].split(" "):
        notification_results = notification_results.filter(
            Q(notification_header__icontains=split_row,) |
            Q(notification_message__icontains=split_row)
        )

    notification_results = notification_results.order_by("notification_header")[:25]

    # Send back json data
    json_results = serializers.serialize("json", notification_results)

    return HttpResponse(json_results, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
def search_organisation(request):
    """
    :param request:
    :return:
    """
    t = loader.get_template("NearBeach/search/search_organisations.html")

    # Get the first 25 organisations
    organisation_results = Organisation.objects.filter(is_deleted=False,).order_by(
        "organisation_name"
    )[:25]

    c = {
        "need_tinymce": True,
        "nearbeach_title": "Search Organisations",
        "organisation_results": serializers.serialize("json", organisation_results),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_organisation_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    organisation_results = Organisation.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data["search"].split(" "):
        # Update the organisation results SQL
        organisation_results = organisation_results.filter(
            organisation_name__icontains=split_row
        )

    # Only have 25 results and order by alphabetical order
    organisation_results = organisation_results.order_by("organisation_name")[:25]

    # Send back json data
    json_results = serializers.serialize("json", organisation_results)

    return HttpResponse(json_results, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def search_permission_set(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Add permissions

    # Get template
    t = loader.get_template("NearBeach/search/search_permission_sets.html")

    # Get data
    permission_set_results = PermissionSet.objects.filter(is_deleted=False,).order_by(
        "permission_set_name"
    )[:25]

    # Get context
    c = {
        "nearbeach_title": "Search Permission Sets",
        "permission_set_results": serializers.serialize("json", permission_set_results),
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_permission_set_data(request):
    """
    :param request:
    :return:
    """
    # Check user permission

    # Get form data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # Get base data
    permission_set_results = PermissionSet.objects.filter(
        is_deleted=False,
    )

    # Loop through the search results
    for split_row in search_form.cleaned_data["search"].split(" "):
        permission_set_results = permission_set_results.filter(
            permission_set_name__icontains=split_row,
        )

    permission_set_results = permission_set_results.order_by("permission_set_name")[:25]

    # Send back json data
    json_results = serializers.serialize("json", permission_set_results)

    return HttpResponse(json_results, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_scheduled_objects(request, *args, **kwargs):
    """
    Will send back a JSON array of Scheduled Objects
    :param request: Contains the POST content for search
    :return: Json Array
    """
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Grab all object assignments for the object template
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
        schedule_object_title__icontains=form.cleaned_data["search"],
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
    return JsonResponse(
        json.loads(scheduled_object_results),
        safe=False
    )


@login_required(login_url="login", redirect_field_name="")
def search_sprint(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Template
    t = loader.get_template("NearBeach/search/search_sprints.html")

    c = {
        "need_tinymce": False,
        "nearbeach_title": "Search Sprints",
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(['POST'])
def search_sprint_data(request):
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the results
    results, count = get_sprint_search_data(form, request)
    results = json.dumps(list(results), cls=DjangoJSONEncoder)

    # Construct Return Results
    return_results = {
        "sprint": json.loads(results),
        "sprint_number_of_pages": math.ceil(count / SEARCH_PAGE_SIZE),
        "sprint_current_page": form.cleaned_data["destination_page"]
    }

    # Return the JSON data
    return JsonResponse(return_results)


@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=1, object_lookup="tag")
def search_tag(request, *args, **kwargs):
    # Get template
    t = loader.get_template("NearBeach/search/search_tags.html")

    # Get data
    tag_results = Tag.objects.filter(
        is_deleted=False,
    ).order_by("tag_name")

    # Context
    c = {
        "need_tinymce": False,
        "tag_results": serializers.serialize("json", tag_results),
        "theme": get_theme(request),
        "user_level": kwargs["user_level"],
    }

    # Send back json data
    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def search_user(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Add permissions

    # Get template
    t = loader.get_template("NearBeach/search/search_users.html")

    # Get Data
    user_results = (
        User.objects.filter()
        .values(
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
        )
        .order_by("last_name", "first_name")[:50]
    )

    # Context
    c = {
        "nearbeach_title": "Search User",
        "user_results": json.dumps(list(user_results), cls=DjangoJSONEncoder),
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def search_user_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    user_results = User.objects.filter()

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data["search"].split(" "):
        # Update the organisation results SQL
        user_results = user_results.filter(
            Q(first_name__icontains=split_row)
            | Q(last_name__icontains=split_row)
            | Q(username__icontains=split_row)
            | Q(email__icontains=split_row)
        )

    # Only have 50 results and order by alphabetical order
    user_results = user_results.values(
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
    ).order_by("last_name", "first_name")[:50]

    # Send back json data
    json_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")
