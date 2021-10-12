# Import Forms
from ..forms import *

# Import Django Libraries
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q

# Import Python Libraries
import json
import urllib.parse
import random

@login_required(login_url='login', redirect_field_name="")
def dashboard(request):
    """
    Due to a bug - if the user goes to /admin/ and logs in there, they will by pass this one session request. It is
    placed here to make sure. :)
    """
    request.session['is_superuser'] = request.user.is_superuser

    # Load the template
    t = loader.get_template('NearBeach/dashboard/dashboard.html')

    # context
    c = {
        'nearbeach_title': 'NearBeach Dashboard',
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def get_bug_list(request):
    """
    :param request:
    :return:
    """
    bug_results = bug.objects.filter(
        is_deleted=False,
        # Add in ability to tell if bugs are opened or closed
    ).values('bug_status').annotate(Count("bug_status"))

    # Send back json data
    json_results = json.dumps(list(bug_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login', redirect_field_name='')
@require_http_methods(['POST'])
def get_my_objects(request):
    """
    :param request:
    :return:
    """
    # Get the user data
    project_results = project.objects.filter(
        is_deleted=False,
        project_id__in=object_assignment.objects.filter(
            is_deleted=False,
            project_id__isnull=False,
            assigned_user=request.user,
        ).values('project_id')
    ).exclude(
        project_status='Closed',
    ).values(
        'project_id',
        'project_name',
        'project_status',
    )

    requirement_results = requirement.objects.filter(
        is_deleted=False,
        requirement_id__in=object_assignment.objects.filter(
            is_deleted=False,
            requirement_id__isnull=False,
            assigned_user=request.user,
        ).values('requirement_id')
    ).exclude(
        requirement_status__requirement_status_is_closed=True,
    ).values(
        'requirement_id',
        'requirement_title',
        'requirement_status__requirement_status',
    )

    task_results = task.objects.filter(
        is_deleted=False,
        task_id__in=object_assignment.objects.filter(
            is_deleted=False,
            task_id__isnull=False,
            assigned_user=request.user,
        ).values('task_id')
    ).exclude(
        task_status='Closed',
    ).values(
        'task_id',
        'task_short_description',
        'task_status',
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
    return JsonResponse({
        'requirement': json.loads(requirement_results),
        'project': json.loads(project_results),
        'task': json.loads(task_results),
    })


@login_required(login_url='login', redirect_field_name='')
@require_http_methods(['POST'])
def get_unassigned_objects(request):
    """
    :param request:
    :return:
    """
    # We only want to look at groups User is connected to
    object_assignment_results=object_assignment.objects.filter(
        is_deleted=False,
        group_id__in=user_group.objects.filter(
            is_deleted=False,
            username=request.user,
        ).values('group_id'),
    )
    
    # Get the user data
    project_results = project.objects.filter(
        is_deleted=False,
        project_id__in=object_assignment_results.filter(
            project_id__isnull=False,
        ).values('project_id')
    ).exclude(
        Q(
            project_status='Closed',
        ) | 
        Q(
            #Project has no users assigned to it
            project_id__in=object_assignment.objects.filter(
                is_deleted=False,
                project_id__isnull=False,
                assigned_user__isnull=False,
            ).values('project_id')
        )
    ).values(
        'project_id',
        'project_name',
        'project_status',
    )

    requirement_results = requirement.objects.filter(
        is_deleted=False,
        requirement_id__in=object_assignment_results.filter(
            requirement_id__isnull=False,
        ).values('requirement_id'),
    ).exclude(
        Q(
            requirement_status__requirement_status_is_closed=True,
        ) |
        Q(
            #Requirement has no users assigned to it
            requirement_id__in=object_assignment.objects.filter(
                is_deleted=False,
                requirement_id__isnull=False,
                assigned_user__isnull=False,
            )
        )
    ).values(
        'requirement_id',
        'requirement_title',
        'requirement_status__requirement_status',
    )

    task_results = task.objects.filter(
        is_deleted=False,
        task_id__in=object_assignment_results.filter(
            task_id__isnull=False,
        ).values('task_id'),
    ).exclude(
        Q(
            task_status='Closed',
        ) |
        Q(
            #Task has no users assigned to it
            task_id__in=object_assignment.objects.filter(
                is_deleted=False,
                task_id__isnull=False,
                assigned_user__isnull=False,
            )
        )
    ).values(
        'task_id',
        'task_short_description',
        'task_status',
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
    #requirement_results = serializers.serialize('json', requirement_results)
    requirement_results = json.dumps(list(requirement_results), cls=DjangoJSONEncoder)
    #project_results = serializers.serialize('json', project_results)
    project_results = json.dumps(list(project_results), cls=DjangoJSONEncoder)
    #task_results = serializers.serialize('json', task_results)
    task_results = json.dumps(list(task_results), cls=DjangoJSONEncoder)

    # Send back a JSON array with JSON arrays inside
    return JsonResponse({
        'requirement': json.loads(requirement_results),
        'project': json.loads(project_results),
        'task': json.loads(task_results),
    })

@login_required(login_url='login', redirect_field_name='')
@require_http_methods(['POST'])
def rfc_approvals(request):
    """
    :param request:
    :return:
    """
    # Get a list of RFC's that are awaiting approval
    rfc_results = request_for_change.objects.filter(
        is_deleted=False,
        rfc_status=2,  # Waiting for approval
    )

    """
    Filter the rfc_results, with any object assignment that the user is currently;
    - A group leader of
    - Connected to an RFC currently waiting for approval
    """
    rfc_results = rfc_results.filter(
        # Filter for any object assignment that is connected by group that user is group leader of.
        rfc_id__in=object_assignment.objects.filter(
            is_deleted=False,
            request_for_change_id__in=rfc_results.values('rfc_id'),
            group_id__in=user_group.objects.filter(
                is_deleted=False,
                username_id=request.user,
                group_leader=True,
            ).values('group_id'),
        ).values('request_for_change_id')
    )

    return HttpResponse(serializers.serialize('json', rfc_results), content_type='application/json')


@login_required(login_url='login', redirect_field_name='')
@require_http_methods(['POST'])
def users_with_no_groups(request):
    """
    """
    # User has to be admin
    if not request.user.is_superuser:
        return HttpResponse()

    # Get all users who do not have a group assigned to them
    user_results = User.objects.filter(
        is_active=True,
    ).exclude(
        # Exclude all users with groups
        id__in=user_group.objects.filter(
            is_deleted=False,
        ).values('username_id')
    ).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )

    # Turn results into json
    json_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')
