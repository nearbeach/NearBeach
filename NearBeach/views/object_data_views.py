from collections import namedtuple
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, CharField, Value as V, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods

import urllib3
import urllib
import json

from NearBeach.models import (
    Bug,
    BugClient,
    ChangeTask,
    Customer,
    Group,
    KanbanCard,
    ObjectAssignment,
    ObjectNote,
    Organisation,
    PermissionSet,
    RequirementItem,
    Tag,
    TagAssignment,
    UserGroup,
)
from NearBeach.views.tools.internal_functions import (
    set_object_from_destination,
    Project,
    Task,
    Requirement,
    get_object_from_destination,
)
from NearBeach.decorators.check_destination import check_destination
from NearBeach.forms import (
    AddBugForm,
    AddCustomerForm,
    AddGroupForm,
    AddObjectLinkForm,
    AddNoteForm,
    AddTagsForm,
    AddUserForm,
    RemoveCustomerForm,
    RemoveGroupForm,
    User,
    DeleteBugForm,
    DeleteLinkForm,
    DeleteTagForm,
    RemoveUserForm,
    SearchForm,
    QueryBugClientForm,
    RemoveLinkForm,
)

from NearBeach.views.tools.lookup_functions import (
    lookup_project,
    lookup_requirement,
    lookup_task,
    lookup_requirement_item
)

# Used for the link list
LOOKUP_FUNCS = {
    "project": lookup_project,
    "task": lookup_task,
    "requirement": lookup_requirement,
    "requirement_item": lookup_requirement_item,
}


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_bug(request, destination, location_id):
    """
    Function to add a bug to an object
    :param: destination: Defines what object the bug is getting added too
    :param: location_id: Defines the object ID that the bug is getting added too
    """
    form = AddBugForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_bug = Bug(
        bug_client=form.cleaned_data["bug_client"],
        bug_code=form.cleaned_data["bug_id"],
        bug_description=form.cleaned_data["bug_description"],
        bug_status=form.cleaned_data["bug_status"],
        change_user=request.user,
    )

    # Connect to the correct destination
    submit_bug = set_object_from_destination(submit_bug, destination, location_id)

    # Save
    submit_bug.save()

    # Get new bug to send back to use
    bug_results = Bug.objects.filter(bug_id=submit_bug.bug_id)

    # Return the JSON data
    return HttpResponse(
        serializers.serialize("json", bug_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_customer(request, destination, location_id):
    """
    Add customer to an object
    :param: destination: the type of object we are adding the customer too
    :param: location_id: the object id we are adding the customer too
    """
    form = AddCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Obtain the data dependent on the destination
    submit_object_assignment = ObjectAssignment(
        change_user=request.user, customer=form.cleaned_data["customer"]
    )
    submit_object_assignment = set_object_from_destination(
        submit_object_assignment, destination, location_id
    )

    # Save the data
    submit_object_assignment.save()

    customer_results = get_customer_list(destination, location_id)

    return HttpResponse(
        serializers.serialize("json", customer_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_group(request, destination, location_id):
    # Get data from form
    form = AddGroupForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # We loop through the responses and add them to the destination's object association
    group_list_results = request.POST.getlist("group_list")

    for single_group in group_list_results:
        # Get group instance
        group_instance = Group.objects.get(group_id=single_group)

        # Construct the object assignment
        submit_object_assignment = ObjectAssignment(
            group_id=group_instance,
            change_user=request.user,
        )
        submit_object_assignment = set_object_from_destination(
            submit_object_assignment, destination, location_id
        )

        # Save the data
        submit_object_assignment.save()

    # Return the updated groups and user back to front end
    return JsonResponse(
        get_group_and_user_list(
            destination,
            location_id,
        )
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_link(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """

    # Get the data
    form = AddObjectLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the parent object of
    object_relation = form.cleaned_data['object_relation']

    # Declaring the dict used in the for loop below
    object_dict = {
        "change_task": ChangeTask.objects,
        "project": Project.objects,
        "task": Task.objects,
        "requirement": Requirement.objects,
        "requirement_item": RequirementItem.objects,
    }

    relation_dict = {
        "relates": "Relate",
        "blocked_by": "Block",
        "blocking": "Block",
        "sub_object_of": "Subobject",
        "parent_object_of": "Subobject",
        "has_duplicate": "Duplicate",
        "duplicate_object": "Duplicate",
    }

    object_title = {
        "change_task": "change_task_title",
        "project": "project_name",
        "task": "task_short_description",
        "requirement": "requirement_title",
        "requirement_item": "requirement_item_title",
    }

    object_status = {
        "change_task": "change_task_status",
        "project": "project_status",
        "task": "task_status",
        "requirement": "requirement_status",
        "requirement_item": "requirement_item_status",
    }

    # Loop through the results and add them in.
    # We will loop through each object type, and add them in accordinly
    for object_type in ["change_task", "project", "task", "requirement", "requirement_item"]:
        # Get the results of each object type and add them
        for row in request.POST.getlist(object_type):
            single_object = object_dict[object_type].get(pk=row)

            submit_object_assignment = ObjectAssignment(
                change_user=request.user, 
                **{object_type: single_object}
            )

            # Set the object destination
            set_object_from_destination(
                submit_object_assignment, destination, location_id
            )

            # Set the parent object if it relates. Depending on the wording - depends if the current
            # Object is the parent object, or not.
            if object_relation in ['relates', 'blocking', 'parent_object_of', 'has_duplicate']:
                submit_object_assignment.parent_link = destination
            else:
                if destination == object_type: 
                    submit_object_assignment.parent_link = "meta_object"
                else:
                    submit_object_assignment.parent_link = object_type

            # Add the link relationship from the dictionary
            submit_object_assignment.link_relationship = relation_dict[object_relation]

            # If object destination is the same as the object type, add the meta_object value
            if destination == object_type:
                # We need to set the meta object
                setattr(submit_object_assignment, "meta_object", row)

                # Update the status and the title with the correct data
                setattr(
                    submit_object_assignment,
                    "meta_object_title",
                    getattr(single_object, object_title[object_type]),
                )

                setattr(
                    submit_object_assignment,
                    "meta_object_status",
                    getattr(single_object, object_status[object_type]),
                )

            submit_object_assignment.save()

    return HttpResponse("Success")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_notes(request, destination, location_id):
    # ADD IN PERMISSIONS HERE!

    # Fill out the form
    form = AddNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # SAVE DATA
    submit_object_note = ObjectNote(
        change_user=request.user, object_note=form.cleaned_data["note"]
    )
    submit_object_note = set_object_from_destination(
        submit_object_note, destination, location_id
    )

    submit_object_note.save()

    # Get data to send back to user
    note_results = ObjectNote.objects.filter(
        object_note_id=submit_object_note.object_note_id
    )

    note_results = note_results.annotate(
        username=F('change_user'),
        first_name=F('change_user__first_name'),
        last_name=F('change_user__last_name'),
        profile_picture=F('change_user__userprofilepicture__document_id__document_key')
    ).values(
        "object_note_id",
        "username",
        "first_name",
        "last_name",
        "profile_picture",
        "object_note",
        "date_modified",
    )

    # Return JSON results
    note_json = json.dumps(list(note_results), cls=DjangoJSONEncoder)

    return HttpResponse(note_json, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_tags(request, destination, location_id):
    # Check the data against the form
    form = AddTagsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Loop throgh each tag
    tag_list_results = request.POST.getlist("tag_id")

    for single_tag in tag_list_results:
        # Grab the tag instance
        tag_instance = Tag.objects.get(tag_id=single_tag)

        submit_tag_assignment = TagAssignment(
            tag=tag_instance,
            object_enum=destination,
            object_id=location_id,
            change_user=request.user,
        )
        submit_tag_assignment.save()

    # Return all tags associated with the destination/locationid
    tag_results = Tag.objects.filter(
        is_deleted=False,
        tag_id__in=TagAssignment.objects.filter(
            is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        ).values("tag_id"),
    )

    return HttpResponse(
        serializers.serialize("json", tag_results),
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def add_user(request, destination, location_id):
    # Check the data against the form
    form = AddUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the list of users from the POST data
    user_list_results = request.POST.getlist("user_list")

    # Loop through them and add them to the object assignment
    for single_user in user_list_results:
        # Get user instance
        user_instance = User.objects.get(id=single_user)

        # Create object assignment
        submit_object_assignment = ObjectAssignment(
            change_user=request.user,
            assigned_user=user_instance,
        )
        submit_object_assignment = set_object_from_destination(
            submit_object_assignment, destination, location_id
        )

        # Save
        submit_object_assignment.save()

    # Return the updated groups and user back to front end
    return JsonResponse(
        get_group_and_user_list(
            destination,
            location_id,
        )
    )

@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def admin_add_user(request):
    """
    :param request:
    :return:
    """
    # Make sure user has permissions
    # Get data
    group_results = Group.objects.filter(
        is_deleted=False,
    ).values()

    permission_set_results = PermissionSet.objects.filter(
        is_deleted=False,
    ).values()

    user_results = User.objects.filter(is_active=True,).values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )

    # Convert data to json format
    group_results = json.dumps(list(group_results), cls=DjangoJSONEncoder)
    permission_set_results = json.dumps(
        list(permission_set_results), cls=DjangoJSONEncoder
    )
    user_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)

    return_data = {
        "group_results": json.loads(group_results),
        "permission_set_results": json.loads(permission_set_results),
        "user_results": json.loads(user_results),
    }

    return JsonResponse(return_data)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def associated_objects(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # Organisations have a special method. We will return the results directly from this method to the user.
    if destination == "organisation":
        return associated_objects_organisations(location_id)

    # Get the data
    object_assignment_results = ObjectAssignment.objects.filter(
        is_deleted=False,
    )
    object_assignment_results = get_object_from_destination(
        object_assignment_results, destination, location_id
    )

    project_results = Project.objects.filter(
        is_deleted=False,
        project_id__in=object_assignment_results.filter(
            project_id__isnull=False
        ).values("project_id"),
    ).values()

    requirement_results = Requirement.objects.filter(
        is_deleted=False,
        requirement_id__in=object_assignment_results.filter(
            requirement_id__isnull=False
        ).values("requirement_id"),
    ).values()

    task_results = Task.objects.filter(
        is_deleted=False,
        task_id__in=object_assignment_results.filter(task_id__isnull=False).values(
            "task_id"
        ),
    ).values()

    # Return the JSON Response back - which will return strait to the user
    return JsonResponse(
        {
            "project": list(project_results),
            "requirement": list(requirement_results),
            "task": list(task_results),
        }
    )


# Internal Functions
def associated_objects_organisations(location_id):
    """
    Due to organisation's links being connected to the objects directly. We will need to query all the objects that
    can be related to an organisation, and combine them into one JSON output.

    To make it JSON friendly, we have to add .values() to each object lookup, and then simple list them in the JSON
    return function below.
    :param location_id:
    :return:
    """
    # Get the data
    project_results = Project.objects.filter(
        is_deleted=False,
        organisation=location_id,
    ).annotate(
        project_status_text=F("project_status__project_status"),
    ).exclude(
        project_status__project_higher_order_status="Closed",
    ).values(
        "project_id",
        "project_name",
        "project_end_date",
        "project_status_text",
    )

    requirement_results = Requirement.objects.filter(
        is_deleted=False,
        organisation=location_id,
    ).annotate(
        requirement_status_text=F("requirement_status__requirement_status"),
    ).exclude(
        requirement_status__requirement_higher_order_status="Closed",
    ).values(
        "requirement_id",
        "requirement_title",
        "requirement_status_text",
    )

    task_results = Task.objects.filter(
        is_deleted=False,
        organisation=location_id,
    ).annotate(
        task_status_text=F("task_status__task_status"),
    ).exclude(
        task_status__task_higher_order_status="Closed",
    ).values(
        "task_id",
        "task_short_description",
        "task_status_text",
        "task_end_date",
    )

    # Return the JSON Response back - which will return strait to the user
    return JsonResponse(
        {
            "project": list(project_results),
            "requirement": list(requirement_results),
            "task": list(task_results),
        }
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def bug_client_list(request):
    bug_client_results = BugClient.objects.filter(
        is_deleted=False,
    )

    return HttpResponse(
        serializers.serialize("json", bug_client_results),
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def bug_list(request, destination, location_id):
    # Obtain the data dependent on the destination
    bug_list_results = Bug.objects.filter(
        is_deleted=False,
    )
    bug_list_results = get_object_from_destination(
        bug_list_results, destination, location_id
    )

    # Limit to certain values
    bug_list_results = bug_list_results.values(
        "bug_id",
        "bug_client",
        "bug_client__list_of_bug_client",
        "bug_client__list_of_bug_client__bug_client_name",
        "bug_client__bug_client_name",
        "bug_client__bug_client_url",
        "bug_code",
        "bug_description",
        "bug_status",
        "project_id",
        "requirement_id",
        "task_id",
    )

    """
    As explained on stack overflow here -
    https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(bug_list_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


# Internal Function
def clean_users_from_object(destination, location_id):
    """
    Problem: There could be users assigned to this object but have no group association. They must be removed from this
    object.
    Solution
    1. Get new list of groups associated with object
    2. From prior list get list of current users for those groups
    3. Grab all users associated with the object, exclude those from prior step
    4. Update and remove those users (as they are no longer associated with this object).
    """
    groups_associated = ObjectAssignment.objects.filter(
        is_deleted=False,
        group_id__isnull=False,
    )
    groups_associated = get_object_from_destination(groups_associated, destination, location_id)

    # Users associated with the groups
    user_list_results = UserGroup.objects.filter(
        is_deleted=False,
        group_id__in=groups_associated.values('group_id'),
    )

    remove_user_list = ObjectAssignment.objects.filter(
        is_deleted=False,
        assigned_user_id__isnull=False,
    ).exclude(
        assigned_user_id__in=user_list_results.values('username_id'),
    )

    remove_user_list = get_object_from_destination(remove_user_list, destination, location_id)

    # Delete what is left
    remove_user_list.update(
        is_deleted=True,
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def customer_list(request, destination, location_id):
    customer_results = get_customer_list(destination, location_id)

    return HttpResponse(
        serializers.serialize("json", customer_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def customer_list_all(request, destination, location_id):
    # Get the organisation dependant on the destination source
    if destination == "requirement":
        organisation_results = Organisation.objects.get(
            organisation_id=Requirement.objects.get(
                is_deleted=False,
                requirement_id=location_id,
            ).organisation_id
        )
    elif destination == "requirement_item":
        organisation_results = Organisation.objects.get(
            organisation_id=Requirement.objects.get(
                is_deleted=False,
                requirement_id=RequirementItem.objects.get(
                    requirement_item_id=location_id
                ).requirement_id,
            ).organisation_id
        )
    elif destination == "project":
        organisation_results = Organisation.objects.get(
            organisation_id=Project.objects.get(
                is_deleted=False,
                project_id=location_id,
            ).organisation_id
        )
    elif destination == "task":
        organisation_results = Organisation.objects.get(
            organisation_id=Task.objects.get(
                is_deleted=False,
                task_id=location_id,
            ).organisation_id
        )
    else:
        # There is no destination that could match this. Send user to errors
        return HttpResponseBadRequest(
            "Sorry - there was an error getting the Customer List"
        )

    customer_results = Customer.objects.filter(
        is_deleted=False, organisation_id=organisation_results.organisation_id
    )

    return HttpResponse(
        serializers.serialize("json", customer_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def delete_bug(request):
    """
    Function will delete a bug - this will remove it from the link tab.

    Function will need to pass the bug id through a form (for checking).
    :param request:
    :return:
    """
    form = DeleteBugForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_bug = form.cleaned_data["bug_id"]
    update_bug.is_deleted = True
    update_bug.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def delete_link(request):
    """
    Function will delete a link - this will remove it from the link tab.

    Function will need to pass the link through a form (for checking).
    :param request:
    :return:
    """
    form = DeleteLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_object_assignment = form.cleaned_data["object_assignment_id"]
    update_object_assignment.is_deleted = True
    update_object_assignment.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def delete_tag(request):
    # Get form data
    form = DeleteTagForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update/Delete tag associations
    TagAssignment.objects.filter(
        is_deleted=False,
        tag_id=form.cleaned_data["tag"],
        object_enum=form.cleaned_data["object_enum"],
        object_id=form.cleaned_data["object_id"],
    ).update(
        is_deleted=True,
    )

    # Ok - return blank
    return HttpResponse("")


# Internal function
def get_customer_list(destination, location_id):
    # Get a list of all objects assignments dependant on the destination
    object_customers = ObjectAssignment.objects.filter(
        is_deleted=False,
        customer_id__isnull=False,
    )
    object_customers = get_object_from_destination(
        object_customers, destination, location_id
    )

    return Customer.objects.filter(
        is_deleted=False, customer_id__in=object_customers.values("customer_id")
    )


# Internal function
def get_group_and_user_list(destination, location_id):
    # Get the data dependant on the objects lookup
    object_group_results = get_group_list(destination, location_id)
    object_user_results = get_user_list(destination, location_id)
    potential_user_results = get_user_list_all(destination, location_id)

    # potential groups are all groups except those in object_group_results
    potential_group_results = Group.objects.filter(
        is_deleted=False,
    ).exclude(
        group_id__in=object_group_results.values('group_id')
    )

    # Convert data to json format
    object_group_results = json.dumps(list(object_group_results.values()), cls=DjangoJSONEncoder)
    potential_group_results = json.dumps(list(potential_group_results.values()), cls=DjangoJSONEncoder)

    return_data = {
        "object_group_list": json.loads(object_group_results),
        "object_user_list": json.loads(object_user_results),
        "potential_group_list": json.loads(potential_group_results),
        "potential_user_list": json.loads(potential_user_results),
    }

    return return_data


# Internal function
def get_group_list(destination, location_id):
    object_results = ObjectAssignment.objects.filter(
        is_deleted=False,
    )
    # If destination is kanban card - use kanban board
    if destination == "kanban_card":
        # Get the card object to obtain the kanban board data
        card_results = KanbanCard.objects.get(kanban_card_id=location_id)

        object_results = get_object_from_destination(
            object_results,
            "kanban_board",
            card_results.kanban_board.kanban_board_id
        )
    else:
        object_results = get_object_from_destination(
            object_results, destination, location_id
        )

    # Now return the groups
    return Group.objects.filter(
        is_deleted=False, group_id__in=object_results.values("group_id")
    )


# Internal Function
def get_user_list(destination, location_id):
    # Get the data we want
    object_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        assigned_user_id__isnull=False,
    )

    # Most times - we will use this function
    object_results = get_object_from_destination(
        object_results, destination, location_id
    )

    # Get the user details
    user_results = User.objects.filter(
        id__in=object_results.values("assigned_user_id")
    ).annotate(
        profile_picture=F('userprofilepicture__document_id__document_key')
    ).values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "profile_picture",
    )

    return json.dumps(list(user_results), cls=DjangoJSONEncoder)


# Internal Function
def get_user_list_all(destination, location_id):
    # Get a list of users we want to exclude
    object_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        assigned_user_id__isnull=False,
    )

    # Get a list of all the groups associated with this destination
    group_results = ObjectAssignment.objects.filter(
        is_deleted=False,
        group_id__isnull=False,
    )

    if destination != "kanban_card":
        object_results = get_object_from_destination(
            object_results, destination, location_id
        )

        group_results = get_object_from_destination(
            group_results, destination, location_id
        )
    else:
        # Get the kanban board information from the card
        kanban_card_results = KanbanCard.objects.get(kanban_card_id=location_id)

        object_results = get_object_from_destination(
            object_results,
            destination,
            location_id
        )

        group_results = get_object_from_destination(
            group_results, "kanban_board", kanban_card_results.kanban_board_id
        )

    # Get a list of users who are associated with these groups & not in the excluded list
    user_results = User.objects.filter(
        id__in=UserGroup.objects.filter(
            is_deleted=False,
            group_id__in=group_results.values("group_id"),
        ).values("username_id"),
        is_active=True,
    ).exclude(
        id__in=object_results.values("assigned_user_id")
    ).annotate(
        profile_picture=F('userprofilepicture__document_id__document_key')
    ).values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "profile_picture",
    )

    return json.dumps(list(user_results), cls=DjangoJSONEncoder)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def group_and_user_data(request, destination, location_id, *args, **kwargs):
    return JsonResponse(
        get_group_and_user_list(
            destination, 
            location_id
        )
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def lead_user_list(request):
    """
    :param request:
    :return:
    """
    # Get the data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # First we create a search string and annotate it onto our results
    user_results = User.objects.annotate(
        search_string=Concat(
            "username",
            V(" "),
            "first_name",
            V(" "),
            "last_name",
            V(" "),
            "email",
            output_field=CharField(),
        )
    ).filter(
        is_active=True,
    )

    for split_row in search_form.cleaned_data["search"].split(" "):
        """ """
        user_results.filter(
            search_string__icontains=split_row,
        )

    # Return the json data
    return HttpResponse(
        serializers.serialize("json", user_results[:25]),
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def link_list(request, destination, location_id, object_lookup):
    # Get user groups
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
        group_id__isnull=False,
    ).values("group_id")

    if object_lookup not in LOOKUP_FUNCS:
        return HttpResponseBadRequest("Sorry - but that object lookup does not exist")

    # Get the data dependent on the object lookup
    data_results = LOOKUP_FUNCS[object_lookup](user_group_results, destination, location_id)

    # Send the data to the user
    data_results = json.dumps(list(data_results), cls=DjangoJSONEncoder)
    return JsonResponse(json.loads(data_results), safe=False)


# Internal function
def link_object(object_assignment_submit, destination, location_id):
    """
    This is an internal function - depending on the destination, depends on what we are linking in the
    object_association_submit
    """
    allowed_destinations = [
        "kanban_board",
        "kanban_card",
        "project",
        "request_for_change",
        "requirement",
        "requirement_item",
        "task",
    ]

    # Double checking that the specified destinations are allowed
    if destination not in allowed_destinations:
        raise PermissionDenied

    object_assignment_submit = object_assignment_submit.filter(
        is_deleted=False, **{destination: location_id}
    )

    # Return the results
    return object_assignment_submit


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def note_list(request, destination, location_id):
    # Everyone should have access to the notes section.

    # Get the notes dependent on the user destination and location
    note_results = ObjectNote.objects.filter(
        is_deleted=False,
    )

    # Filter by destination and location_id
    note_results = get_object_from_destination(note_results, destination, location_id)

    # Filter for the fields that we want
    note_results = note_results.annotate(
        username=F('change_user'),
        first_name=F('change_user__first_name'),
        last_name=F('change_user__last_name'),
        profile_picture=F('change_user__userprofilepicture__document_id__document_key')
    ).values(
        "object_note_id",
        "username",
        "first_name",
        "last_name",
        "profile_picture",
        "object_note",
        "date_modified",
    )

    # Return JSON results
    note_json = json.dumps(list(note_results), cls=DjangoJSONEncoder)

    return HttpResponse(note_json, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def object_link_list(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    object_assignment_results = ObjectAssignment.objects.filter(
        is_deleted=False,
    )

    # Check objects that match the destination and location id
    # Also make sure we get any meta data where the destination is not null
    object_assignment_results = object_assignment_results.filter(
        Q(
            # Where destination and location id match
            **{destination: location_id},
        )
        | Q(
            **{destination + "__isnull": False},
            meta_object=location_id,
        )
    )

    # Separate each section into;
    # - projects
    # - tasks
    # - requirements
    # - requirement items
    # - meta
    ObjectStructure = namedtuple(
        "ObjectStructure",
        ["object_id", "object_title", "object_status", "object_type", "non_null_field"]    
    )

    data_point_list = [
        ObjectStructure("project_id", "project_id__project_name", "project_id__project_status__project_status", "project","project"),
        ObjectStructure("task_id", "task_id__task_short_description", "task_id__task_status__task_status", "task", "task"),
        ObjectStructure("requirement_id", "requirement_id__requirement_title", "requirement_id__requirement_status__requirement_status", "requirement", "requirement"),
        ObjectStructure("requirement_item_id", "requirement_item_id__requirement_item_title", "requirement_item_id__requirement_item_status__requirement_item_status", "requirement_item", "requirement_item"),
        ObjectStructure("meta_object", "meta_object_title", "meta_object_status", destination, "meta_object"),
    ]

    data_results = []
    for data_point in data_point_list:
        # When the destination == non_null_field, we specifically want to check out all meta_objects 
        # that equal the location id. We want to make sure;
        # 1. the destination column is not null
        # 2. the meta_object == location_id
        # These will be all meta_object assigned to the current object
        if destination == data_point.non_null_field:
            data_results.extend(object_assignment_results.filter(
                meta_object=location_id,
                **{destination + "__isnull": False},
            ).annotate(
                object_id=F(data_point.object_id),
                object_title=F(data_point.object_title),
                object_status=F(data_point.object_status),
                object_type=V(data_point.object_type),
                reverse_relation=V(True),
            ).values(
                "object_id",
                "object_title",
                "object_status",
                "object_type", 
                "link_relationship",
                "parent_link",
                "reverse_relation",
            ))
        else:
            # The following looks at the other fields, where the object is assigned to it's associated
            # object field (and not meta). i.e. project is in project column.
            data_results.extend(object_assignment_results.filter(
                    **{data_point.non_null_field + "__isnull": False},
            ).exclude(
                meta_object=location_id,
            ).annotate(
                object_id=F(data_point.object_id),
                object_title=F(data_point.object_title),
                object_status=F(data_point.object_status),
                object_type=V(data_point.object_type),
                reverse_relation=V(False),
            ).values(
                "object_id",
                "object_title",
                "object_status",
                "object_type", 
                "link_relationship",
                "parent_link",
                "reverse_relation",
            ))

    # If the destination is either a project, task, or requirement - add on kanban cards
    if destination in ["project", "task", "requirement"]:
        data_results.extend(KanbanCard.objects.filter(
            # **{data_point.non_null_field + "__isnull": False},
            **{destination + "_id": location_id}
        ).annotate(
            object_id=F("kanban_card_id"),
            object_title=F("kanban_card_text"),
            object_status=F("kanban_column_id__kanban_column_name"),
            object_type=V("card"),
            reverse_relation=V(False),
            link_relationship=V("Card"),
            parent_link=V("card"),
        ).values(
            "object_id",
            "object_title",
            "object_status",
            "object_type",
            "link_relationship",
            "parent_link",
            "reverse_relation",
        ))

    return JsonResponse(data_results, safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def query_bug_client(request, destination, location_id):
    # Insert data into form
    form = QueryBugClientForm(request.POST)

    # Check to make sure everything is fine with the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the information from the form
    bug_client_instance = form.cleaned_data["bug_client_id"]
    _ = form.cleaned_data["search"]

    # Get existing bugs that we want to extract out
    existing_bugs = Bug.objects.filter(
        is_deleted=False,
        bug_client_id=bug_client_instance.bug_client_id,
    )
    existing_bugs = get_object_from_destination(existing_bugs, destination, location_id)

    # The values in the URL
    f_bugs = ""
    o_notequals = ""
    v_values = ""

    # The for loop
    for idx, row in enumerate(existing_bugs):
        nidx = str(idx + 1)
        f_bugs = f_bugs + "&f" + nidx + "=bug_id"
        o_notequals = o_notequals + "&o" + nidx + "=notequals"
        v_values = v_values + "&v" + nidx + "=" + str(row.bug_code)

    exclude_url = f_bugs + o_notequals + v_values

    url = (
        bug_client_instance.bug_client_url
        + bug_client_instance.list_of_bug_client.bug_client_api_url
        + bug_client_instance.list_of_bug_client.api_search_bugs
        + urllib.parse.quote(form.cleaned_data["search"])
        + exclude_url
    )

    """
    SECURITY ISSUE
    ~~~~~~~~~~~~~~
    The URL could contain a file. Which we do not want executed by mistake. So we just make sure that the URL starts
    with a http instead of ftp or file.

    We place the  at the end of the json_data because we have checked the field. This should be just a json
    response. If it is not at this point then it will produce a server issue.
    """
    if url.lower().startswith("http"):
        # setup the pool manager for urllib3
        http = urllib3.PoolManager()

        # Plug in the url
        r = http.request("GET", url)

        # Extract the data
        json_data = json.loads(r.data.decode("utf-8"))
    else:
        raise ValueError from None

    # Send back the JSON data
    return JsonResponse(json_data["bugs"], safe=False)


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def remove_customer(request, destination, location_id):
    # Get the form data
    form = RemoveCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_object_assignment = ObjectAssignment.objects.filter(
        customer_id=form.cleaned_data["customer_id"],
    )

    # Using internal functions - get the relevant data
    update_object_assignment = link_object(
        update_object_assignment, destination, location_id
    )

    # Update and save data
    update_object_assignment.update(
        is_deleted=True,
    )

    return HttpResponse("") 


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def remove_group(request, destination, location_id):
    # Get the form data
    form = RemoveGroupForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_object_assignment = ObjectAssignment.objects.filter(
        group_id=form.cleaned_data["group_id"],
    )

    # Using internal functions - get the relevant data
    update_object_assignment = link_object(
        update_object_assignment, destination, location_id
    )

    # Update and save data
    update_object_assignment.update(
        is_deleted=True,
    )

    # Remove any users that no longer have a group associated with this object
    clean_users_from_object(destination, location_id)

    # Return the updated groups and user back to front end
    return JsonResponse(
        get_group_and_user_list(
            destination,
            location_id,
        )
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def remove_link(request, destination, location_id):
    form = RemoveLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Now we limit the data to what we want, and then soft delete it
    ObjectAssignment.objects.filter(
        is_deleted=False,
        **{destination: location_id},
        **{form.cleaned_data["link_connection"]: form.cleaned_data["link_id"]},
    ).update(is_deleted=True)

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def remove_user(request, destination, location_id):
    # Get the form data
    form = RemoveUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the user instance
    user_instance = User.objects.get(username=form.cleaned_data["username"])

    # Delete user from object assignment for destination and location_id
    update_object_assignment = ObjectAssignment.objects.filter(
        assigned_user=user_instance,
    )

    # Using internal functions - get the relevant data
    update_object_assignment = link_object(
        update_object_assignment, destination, location_id
    )

    # Update and save data
    update_object_assignment.update(
        is_deleted=True,
    )

    # Return the updated groups and user back to front end
    return JsonResponse(
        get_group_and_user_list(
            destination,
            location_id,
        )
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def tag_list(request, destination, location_id):
    # Get the data we want
    tag_results = Tag.objects.filter(
        is_deleted=False,
        tag_id__in=TagAssignment.objects.filter(
            is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        ).values("tag_id"),
    )

    return HttpResponse(
        serializers.serialize("json", tag_results),
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def tag_list_all(request):
    # Get the data we want
    tag_results = Tag.objects.filter(
        is_deleted=False,
    )

    return HttpResponse(
        serializers.serialize("json", tag_results),
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_destination()
def user_list(request, destination, location_id):
    # Get the data we want
    user_results = get_user_list(destination, location_id)

    return HttpResponse(user_results, content_type="application/json")



#     # Get Data we want

#     # Send back json data

#     return HttpResponse(json_results, content_type="application/json")
