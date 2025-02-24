from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.db.models import F, Value as V
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods

from NearBeach.forms import MyPlannerAddObjectForm, MyPlannerUpdateObjectListForm, MyPlannerDeleteUserJobForm
from NearBeach.models import KanbanCard, ObjectAssignment, Project, Task, UserJob

import datetime
import json

from NearBeach.views.theme_views import get_theme


DICT_PLANNING_OBJECTS = {
    "kanban_card": {
        "object": KanbanCard,
        "destination": "kanban_card",
        "location_id": "kanban_card_id",
        "title": "kanban_card_text",
        "status": "kanban_column__kanban_column_name",
        "higher_order_status": "kanban_column__kanban_column_property",
        "end_date": "",
    },
    "project": {
        "object": Project,
        "destination": "project",
        "location_id": "project_id",
        "title": "project_name",
        "status": "project_status__project_status",
        "higher_order_status": "project_status__project_higher_order_status",
        "end_date": "project_end_date",
    },
    "task": {
        "object": Task,
        "destination": "task",
        "location_id": "task_id",
        "title": "task_short_description",
        "status": "task_status__task_status",
        "higher_order_status": "task_status__task_higher_order_status",
        "end_date": "task_end_date",
    },
}


# Internal Function
def get_my_planning_objects(request, delta=7):
    # Lowest delta is a 1
    delta = max(delta, 1)

    # Get todays date
    today = datetime.date.today()

    # Get all user jobs within the next 7 days
    userjob_results = UserJob.objects.filter(
        is_deleted=False,
        username=request.user.id,
        job_date__gte=today,
        job_date__lt=today + datetime.timedelta(days=delta),
    )

    project_results = userjob_results.filter(
        is_deleted=False,
        project__isnull=False,
    ).annotate(
        object_type=V("project"),
        location_id=F("project_id"),
        title=F("project__project_name"),
        end_date=F("project__project_end_date"),
        status=F("project__project_status__project_status"),
        higher_order_status=F("project__project_status__project_higher_order_status"),
    ).values(
        "user_job_id",
        "object_type",
        "location_id",
        "title",
        "end_date",
        "status",
        "higher_order_status",
        "job_date",
        "job_sort_number",
    )

    task_results = userjob_results.filter(
        is_deleted=False,
        task__isnull=False,
    ).annotate(
        object_type=V("task"),
        location_id=F("task_id"),
        title=F("task__task_short_description"),
        end_date=F("task__task_end_date"),
        status=F("task__task_status__task_status"),
        higher_order_status=F("task__task_status__task_higher_order_status"),
    ).values(
        "user_job_id",
        "object_type",
        "location_id",
        "title",
        "end_date",
        "status",
        "higher_order_status",
        "job_date",
        "job_sort_number",
    )

    card_results = userjob_results.filter(
        is_deleted=False,
        kanban_card__isnull=False,
        kanban_card__is_archived=False,
    ).annotate(
        object_type=V("kanban_card"),
        location_id=F("kanban_card__kanban_card_id"),
        title=F("kanban_card__kanban_card_text"),
        end_date=V(""),
        status=F("kanban_card__kanban_column__kanban_column_name"),
        higher_order_status=F("kanban_card__kanban_column__kanban_column_property"),
    ).values(
        "user_job_id",
        "object_type",
        "location_id",
        "title",
        "end_date",
        "status",
        "higher_order_status",
        "job_date",
        "job_sort_number",
    )

    results = list(project_results) + list(task_results) + list(card_results)

    return json.dumps(results, cls=DjangoJSONEncoder)


@login_required(login_url="login", redirect_field_name="")
def my_planner(request):
    # Template
    t = loader.get_template("NearBeach/my_planner/my_planner.html")

    results = get_my_planning_objects(request, 7)

    c = {
        "nearbeach_title": "My Planner",
        "object_data": json.loads(results),
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def my_planner_add_object(request):
    form = MyPlannerAddObjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Grab the destination from the form
    destination = form.cleaned_data['destination']

    # Check the destination
    if destination not in ["kanban_card", "project", "task"]:
        return HttpResponseBadRequest("Sorry - destination does not exist")

    # Get the job sort number
    job_sort_number = len(UserJob.objects.filter(
        is_deleted=False,
        job_date=form.cleaned_data["job_date"],
        username=request.user
    ))

    # Loop through the results from POST.GetLIST
    for row in request.POST.getlist(destination):
        # Create a new row in the user job
        submit_user_job = UserJob(
            username=request.user,
            job_date=form.cleaned_data["job_date"],
            job_sort_number=job_sort_number,
            change_user=request.user,
        )

        # Grab the object we require
        dict_object = DICT_PLANNING_OBJECTS[destination]
        object_results = dict_object["object"].objects.get(
            pk=row,
        )

        # Set the attribute for the object
        setattr(submit_user_job, destination, object_results)

        # Iterate on the job_sort_number
        job_sort_number = job_sort_number + 1

        submit_user_job.save()

    results = get_my_planning_objects(request, 7)

    return JsonResponse(json.loads(results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def my_planner_delete_user_job(request):
    form = MyPlannerDeleteUserJobForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Delete the data
    user_job_update = form.cleaned_data["user_job_id"]

    # Check permissions. Username should match current logged in user
    if not user_job_update.username == request.user:
        return HttpResponseBadRequest("Can't modify other users")

    user_job_update.is_deleted = True
    user_job_update.save()

    return HttpResponse()


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def my_planner_get_object_list(request, destination):
    # Make sure the destination is correct
    if destination not in ["kanban_card", "project", "task"]:
        return HttpResponseBadRequest("Wrong object within destination")

    # Get all objects assigned to the user
    object_assignment_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        **{F"{destination}__isnull": False},
        assigned_user=request.user,
    ).annotate(
        object_id=F(F"{destination}_id")
    ).values(
        "object_id",
    )

    # Check to make sure the kanban cards are not archived
    if destination == "kanban_card":
        object_assignment_results = object_assignment_results.filter(
            kanban_card__is_archived=False,
        )

    # Using the list of ids. We now grab the objects
    dict_object = DICT_PLANNING_OBJECTS[destination]

    results = dict_object["object"].objects.filter(
        is_deleted=False,
        **{F"{destination}_id__in": object_assignment_results.values("object_id")},
    ).exclude(
        **{F"{dict_object['higher_order_status']}": "Closed"},
    ).annotate(
        destination=V(dict_object["destination"]),
        location_id=F(dict_object["location_id"]),
        title=F(dict_object["title"]),
        status=F(dict_object["status"]),
    ).values(
        "destination",
        "location_id",
        "title",
        "status",
    )

    # Convert to JSON
    results = json.dumps(list(results), cls=DjangoJSONEncoder)

    return JsonResponse(json.loads(results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@require_http_methods(["POST"])
def my_planner_update_object_list(request):
    form = MyPlannerUpdateObjectListForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the user job
    user_job_update = form.cleaned_data["user_job_id"]
    user_job_update.job_date = form.cleaned_data["job_date"]

    # Check to make sure the user job username is the request username
    if not user_job_update.username == request.user:
        return HttpResponseBadRequest("Can't modify other users")

    # Update the sort order.
    # old_destination is optional
    new_destination = form.cleaned_data['new_destination']
    old_destination = form.cleaned_data['old_destination']

    for index, card in enumerate(new_destination):
        if card.user_job_id == user_job_update.user_job_id:
            user_job_update.job_sort_number = index
            user_job_update.save()
        else:
            card.job_sort_number = index
            card.save()

    for index, card in enumerate(old_destination):
        card.job_sort_number = index
        card.save()

    return HttpResponse("")
