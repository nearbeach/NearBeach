from ..forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q, F
from django.contrib.auth.models import User

# Import Python Libraries
import json, datetime

# Import NearBeach Models
from NearBeach.models import (
    Bug,
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    Notification,
    ObjectAssignment,
    Project,
    RequestForChange,
    Requirement,
    Task,
    UserGroup,
)
from NearBeach.views.theme_views import get_theme
from NearBeach.views.user_job_views import get_my_planning_objects
from ..utils.enums.request_for_change_enums import RequestForChangeStatus


@login_required(login_url="login", redirect_field_name="")
def dashboard(request):
    """
    Due to a bug - if the user goes to /admin/ and logs in there, they will by pass this one session request. It is
    placed here to make sure. :)
    """
    request.session["is_superuser"] = request.user.is_superuser

    # Load the template
    t = loader.get_template("NearBeach/dashboard/dashboard.html")

    # Get notification results
    notification_results = Notification.objects.filter(
        Q(
            is_deleted=False,
            notification_start_date__lte=datetime.datetime.now().date(),
            notification_end_date__gte=datetime.datetime.now().date(),
        )
        & Q(Q(notification_location="all") | Q(notification_location="dashboard"))
    )

    # context
    c = {
        "nearbeach_title": "NearBeach Dashboard",
        "need_tinymce": False,
        "notification_results": notification_results,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def get_bug_list(request):
    """
    Gets a list of all the bugs
    :param request:
    :return:
    """
    bug_results = (
        Bug.objects.filter(
            is_deleted=False,
            # Add in ability to tell if bugs are opened or closed
        )
        .values("bug_status")
        .annotate(Count("bug_status"))
    )

    # Send back json data
    json_results = json.dumps(list(bug_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def get_kanban_list(request):
    """Gets a list of all kanban's the users assigned to"""
    object_assignment_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        kanban_board_id__isnull=False,
        group_id__in=UserGroup.objects.filter(
            is_deleted=False, username=request.user
        ).values("group_id"),
    )

    kanban_results = KanbanBoard.objects.filter(
        is_deleted=False,
        kanban_board_status="Open",
        kanban_board_id__in=object_assignment_results.values("kanban_board_id"),
    )

    # Send back json data
    return HttpResponse(
        serializers.serialize("json", kanban_results), content_type="application/json"
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def get_my_objects(request):
    """
    Get any objects the user is assigned too
    :param request:
    :return:
    """
    # Get the user data
    project_results = (
        Project.objects.filter(
            is_deleted=False,
            project_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                project_id__isnull=False,
                assigned_user=request.user,
            ).values("project_id"),
        )
        .exclude(
            project_status__project_higher_order_status="Closed",
        )
        .values(
            "project_id",
            "project_name",
            "project_status__project_status",
            "project_end_date",
        )
    )

    requirement_results = (
        Requirement.objects.filter(
            is_deleted=False,
            requirement_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                requirement_id__isnull=False,
                assigned_user=request.user,
            ).values("requirement_id"),
        )
        .exclude(
            requirement_status__requirement_higher_order_status="Closed",
        )
        .values(
            "requirement_id",
            "requirement_title",
            "requirement_status__requirement_status",
        )
    )

    task_results = (
        Task.objects.filter(
            is_deleted=False,
            task_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                task_id__isnull=False,
                assigned_user=request.user,
            ).values("task_id"),
        )
        .exclude(
            task_status__task_higher_order_status="Closed",
        )
        .values(
            "task_id",
            "task_short_description",
            "task_status__task_status",
            "task_end_date",
        )
    )

    kanban_board_results = (
        KanbanBoard.objects.filter(
            is_deleted=False,
            kanban_board_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                kanban_board_id__isnull=False,
                assigned_user=request.user,
            ).values("kanban_board_id")
        )
        .exclude(
            kanban_board_status="Closed",
        )
        .values(
            "kanban_board_id",
            "kanban_board_name",
            "kanban_board_status",
        )
    )

    card_results = (
        KanbanCard.objects.filter(
            is_deleted=False,
            kanban_card_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                kanban_card_id__isnull=False,
                assigned_user=request.user,
            ).values("kanban_card_id"),
            kanban_board__kanban_board_status="Open",
        )
        .exclude(
            Q(
                # Exclude cards that are archived
                is_archived=True,
            )
            | Q(
                # Exclude cards that are inside columns that are closed
                kanban_column_id__in=KanbanColumn.objects.filter(
                    is_deleted=False,
                    kanban_column_property="Closed",
                )
            )
        )
        .values(
            "kanban_card_id",
            "kanban_card_text",
            "kanban_column__kanban_column_name",  # Check this field
        )
    )

    # Only have 25 results and order by alphabetical order
    # requirement_results.order_by('requirement_title')[:25]
    # project_results.order_by('project_name')[:25]
    # task_results.order_by('task_short_description').values()[:25]

    """
    The pain point
    ~~~~~~~~~~~~~~
    Due to Django wanting to send converted json data as a string, we have to;
    1. Apply serialisation
    2. Apply a json.loads function
    3. Compile data and send back.

    Note to Django developers - there has to be a better way
    """
    requirement_results = json.dumps(list(requirement_results), cls=DjangoJSONEncoder)
    project_results = json.dumps(list(project_results), cls=DjangoJSONEncoder)
    task_results = json.dumps(list(task_results), cls=DjangoJSONEncoder)
    kanban_board_results = json.dumps(list(kanban_board_results), cls=DjangoJSONEncoder)
    card_results = json.dumps(list(card_results), cls=DjangoJSONEncoder)

    # Send back a JSON array with JSON arrays inside
    return JsonResponse(
        {
            "requirement": json.loads(requirement_results),
            "project": json.loads(project_results),
            "task": json.loads(task_results),
            "kanban_board": json.loads(kanban_board_results),
            "card": json.loads(card_results),
        }
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def get_todo_today(request):
    """
    Function returns the user's to-do list they have setup for today.

    We utilise the same function user in the my planner section
    """
    results = get_my_planning_objects(request, 1)

    return JsonResponse(json.loads(results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def get_unassigned_objects(request):
    """
    Function returns an json array with data from;
    - Projects
    - Requirements
    - Tasks

    Please note - a user who does not have project/task/requirement access for a
    certain group, will not have said object return. Hence the partial checks like;
    `permission_set__project__gt=0,`
    Where we make sure the user has at least read only access.
    :param request:
    :return:
    """
    project_results = (
        Project.objects.filter(
            is_deleted=False,
            project_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id__in=UserGroup.objects.filter(
                    is_deleted=False,
                    username=request.user,
                    # We want to make sure the user's permissions for this particular
                    # Project, is greater than zero.
                    permission_set__project__gt=0,
                ).values("group_id"),
            ).values("project_id"),
        )
        .exclude(
            Q(
                project_status__project_higher_order_status="Closed",
            )
            | Q(
                # Project has no users assigned to it
                project_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    project_id__isnull=False,
                    assigned_user__isnull=False,
                ).values("project_id")
            )
        )
        .values(
            "project_id",
            "project_name",
            "project_status__project_status",
            "project_end_date",
        )
    )
    requirement_results = (
        Requirement.objects.filter(
            is_deleted=False,
            requirement_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id__in=UserGroup.objects.filter(
                    is_deleted=False,
                    username=request.user,
                    # We want to make sure the user's permissions for this particular
                    # Requirements, is greater than zero.
                    permission_set__requirement__gt=0,
                ).values("group_id"),
            ).values("requirement_id"),
        )
        .exclude(
            Q(
                requirement_status__requirement_higher_order_status="Closed",
            )
            | Q(
                # Requirement has no users assigned to it
                requirement_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    requirement_id__isnull=False,
                    assigned_user__isnull=False,
                ).values("requirement_id")
            )
        )
        .values(
            "requirement_id",
            "requirement_title",
            "requirement_status__requirement_status",
        )
    )

    task_results = (
        Task.objects.filter(
            is_deleted=False,
            task_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id__in=UserGroup.objects.filter(
                    is_deleted=False,
                    username=request.user,
                    # We want to make sure the user's permissions for this particular
                    # Tasks, is greater than zero.
                    permission_set__task__gt=0,
                ).values("group_id"),
            ).values("task_id"),
        )
        .exclude(
            Q(
                task_status__task_higher_order_status="Closed",
            )
            | Q(
                # Task has no users assigned to it
                task_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    task_id__isnull=False,
                    assigned_user__isnull=False,
                ).values("task_id")
            )
        )
        .values(
            "task_id",
            "task_short_description",
            "task_status__task_status",
            "task_end_date",
        )
    )
    # Only have 25 results and order by alphabetical order
    # requirement_results.order_by('requirement_title')[:25]
    # project_results.order_by('project_name')[:25]
    # task_results.order_by('task_short_description').values()[:25]

    """
    The pain point
    ~~~~~~~~~~~~~~
    Due to Django wanting to send converted json data as a string, we have to;
    1. Apply serialisation
    2. Apply a json.loads function
    3. Compile data and send back.

    Note to Django developers - there has to be a better way
    """
    requirement_results = json.dumps(list(requirement_results), cls=DjangoJSONEncoder)
    project_results = json.dumps(list(project_results), cls=DjangoJSONEncoder)
    task_results = json.dumps(list(task_results), cls=DjangoJSONEncoder)

    # Send back a JSON array with JSON arrays inside
    return JsonResponse(
        {
            "requirement": json.loads(requirement_results),
            "project": json.loads(project_results),
            "task": json.loads(task_results),
        }
    )


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def rfc_approvals(request):
    """
    Will get the rfc approvals that the user will need to approve
    :param request:
    :return:
    """
    # Get a list of RFC's that are awaiting approval
    rfc_results = RequestForChange.objects.filter(
        is_deleted=False,
        rfc_status=RequestForChangeStatus.WAITING_FOR_APPROVAL,  # Waiting for approval
    )

    """
    Filter the rfc_results, with any object assignment that the user is currently;
    - A group leader of
    - Connected to an RFC currently waiting for approval
    """
    rfc_results = rfc_results.filter(
        # Filter for any object assignment that is connected by group that user is group leader of.
        rfc_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            request_for_change_id__in=rfc_results.values("rfc_id"),
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username_id=request.user,
                group_leader=True,
            ).values("group_id"),
        ).values("request_for_change_id")
    ).values(
        "rfc_id",
        "rfc_title",
        "rfc_status",
        # "rfc_status__rfc_status",
    )

    # Turn results into json
    json_results = json.dumps(list(rfc_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def users_with_no_groups(request):
    """ """
    # User has to be admin
    if not request.user.is_superuser:
        return HttpResponse()

    # Get all users who do not have a group assigned to them
    user_results = (
        User.objects.filter(
            is_active=True,
        )
        .exclude(
            # Exclude all users with groups
            id__in=UserGroup.objects.filter(
                is_deleted=False,
            ).values("username_id")
        ).annotate(
            profile_picture=F('userprofilepicture__document_id__document_key')
        )
        .values(
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
        )
    )

    # Turn results into json
    json_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")
