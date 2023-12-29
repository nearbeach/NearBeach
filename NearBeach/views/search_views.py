import json
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, F
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from NearBeach.forms import SearchObjectsForm, SearchForm
from NearBeach.decorators.check_user_permissions import check_user_permissions
from NearBeach.models import (
    Notification,
    ObjectAssignment,
    RequestForChange,
    Requirement,
    Project,
    Task,
    KanbanBoard,
    ListOfRequirementStatus,
    Customer,
    Group,
    Organisation,
    PermissionSet,
    User,
    Tag,
    UserGroup,
)
from NearBeach.views.theme_views import get_theme
from NearBeach.decorators.check_user_permissions import check_user_admin_permissions


# Internal Function
def get_object_search_data(search_form, request):
    """
    The following internal function will search the following objects using the form's data;
    - Kanban boards
    - Request for Change
    - Requirements
    - Projects
    - Tasks
    It will combine them into a single JSON array and send back to the previous function
    :param form: Contains all the data we require.
    :return:
    """
    # Get instance data for all objects
    rfc_results = RequestForChange.objects.filter(is_deleted=False,).values(
        "rfc_id",
        "rfc_title",
        "rfc_status",
        "rfc_status__rfc_status",
    )
    requirement_results = Requirement.objects.filter(is_deleted=False,).values(
        "requirement_id",
        "requirement_title",
        "requirement_status__requirement_status",
    )
    project_results = Project.objects.filter(is_deleted=False,).annotate(
        project_status_text=F("project_status__project_status"),
    ).values(
        "project_id",
        "project_name",
        "project_status_text",
    )
    task_results = Task.objects.filter(is_deleted=False,).annotate(
        task_status_text=F("task_status__task_status"),
    ).values(
        "task_id",
        "task_short_description",
        "task_status_text",
    )
    kanban_results = KanbanBoard.objects.filter(is_deleted=False,).values(
        "kanban_board_id",
        "kanban_board_name",
        "kanban_board_status",
    )

    # Check to see if not superuser - if not we limit to user's own groups
    if not request.user.is_superuser:
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values("group_id"),
        )

        rfc_results = rfc_results.filter(
            rfc_id__in=object_assignment_results.filter(
                request_for_change_id__isnull=False,
            ).values("request_for_change_id"),
        )

        requirement_results = requirement_results.filter(
            requirement_id__in=object_assignment_results.filter(
                requirement_id__isnull=False,
            ).values("requirement_id"),
        )

        project_results = project_results.filter(
            project_id__in=object_assignment_results.filter(
                project_id__isnull=False,
            ).values("project_id"),
        )

        task_results = task_results.filter(
            task_id__in=object_assignment_results.filter(
                task_id__isnull=False,
            ).values("task_id"),
        )

        kanban_results = kanban_results.filter(
            kanban_board_id__in=object_assignment_results.filter(
                kanban_board_id__isnull=False,
            ).values("kanban_board_id"),
        )

    # Check to see if we are searching for closed objects
    include_closed = search_form.cleaned_data["include_closed"]

    # If we are NOT including closed - then we will limit to those with status is_deleted=False
    if not include_closed:
        rfc_results = rfc_results.exclude(
            rfc_status__in=(5, 6),
        )

        requirement_results = requirement_results.exclude(
            requirement_status__in=ListOfRequirementStatus.objects.filter(
                is_deleted=False,
                # requirement_status_is_closed=True,
                requirement_higher_order_status="Closed",
            ).values("requirement_status_id")
        )

        project_results = project_results.exclude(
            # project_status__in=["Closed"],
            project_status__project_higher_order_status="Closed",
        )

        task_results = task_results.exclude(
            # task_status__in=["Closed"],
            task_status__task_higher_order_status="Closed",
        )

        kanban_results = kanban_results.exclude(
            kanban_board_status__in=["Closed"],
        )

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data["search"].split(" "):
        # Update the each instance with the split row results
        rfc_results = rfc_results.filter(Q(rfc_title__icontains=split_row))
        requirement_results = requirement_results.filter(
            Q(requirement_title__icontains=split_row)
        )
        project_results = project_results.filter(Q(project_name__icontains=split_row))
        task_results = task_results.filter(
            Q(task_short_description__icontains=split_row)
        )
        kanban_results = kanban_results.filter(
            Q(kanban_board_name__icontains=split_row)
        )

        # If the split row is a number - also check against the id
        if split_row.isnumeric():
            rfc_results = rfc_results.filter(Q(rfc_id=split_row))
            requirement_results = requirement_results.filter(
                Q(requirement_id=split_row)
            )
            project_results = project_results.filter(Q(project_id=split_row))
            task_results = task_results.filter(Q(task_id=split_row))
            kanban_results = kanban_results.filter(Q(kanban_board_id=split_row))
    # Only have 25 results and order by alphabetical order
    rfc_results = rfc_results.order_by("rfc_title")[:25]
    requirement_results = requirement_results.order_by("requirement_title")[:25]
    project_results = project_results.order_by("project_name")[:25]
    task_results = task_results.order_by("task_short_description")[:25]
    kanban_results = kanban_results.order_by("kanban_board_name")[:25]

    """
    The pain point
    ~~~~~~~~~~~~~~
    Due to Django wanting to send converted json data as a string, we have to;
    1. Apply serialisation
    2. Apply a json.loads function
    3. Compile data and send back.

    Note to Django developers - there has to be a better way
    """
    rfc_results = json.dumps(list(rfc_results), cls=DjangoJSONEncoder)
    requirement_results = json.dumps(list(requirement_results), cls=DjangoJSONEncoder)
    project_results = json.dumps(list(project_results), cls=DjangoJSONEncoder)
    task_results = json.dumps(list(task_results), cls=DjangoJSONEncoder)
    kanban_results = json.dumps(list(kanban_results), cls=DjangoJSONEncoder)

    # Send back a JSON array with JSON arrays inside
    return {
        "request_for_change": json.loads(rfc_results),
        "requirement": json.loads(requirement_results),
        "project": json.loads(project_results),
        "task": json.loads(task_results),
        "kanban": json.loads(kanban_results),
    }


@login_required(login_url="login", redirect_field_name="")
def search(request):
    """
    :param request:
    :return:
    """
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Template
    t = loader.get_template("NearBeach/search/search.html")

    # Translate the include closed, from Python Boolean to JavaScript boolean
    if form.cleaned_data["include_closed"]:  # If exists and true
        include_closed = "true"
    else:
        include_closed = "false"

    # Context
    c = {
        "include_closed": include_closed,
        "need_tinymce": False,
        "nearbeach_title": "Search",
        "search_input": form.cleaned_data["search"],
        "search_results": get_object_search_data(form, request),
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

    # Return the JSON data
    return JsonResponse(get_object_search_data(form, request))


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

    notification_results = Notification.objects.filter()

    c = {
        "need_tinymce": False,
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
    notification_results = Notification.objects.filter()

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


@login_required(login_url="login", redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup="tag")
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
