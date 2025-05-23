import django.forms
from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.db.models import F, Value, Q
from django.db.models.functions import Concat
from django.template.loader import get_template
from NearBeach.views.theme_views import get_theme
from NearBeach.forms import GdprObjectTypeForm, GdprDataRequestForm, GdprObjectSubmitForm
from NearBeach.models import (
    Customer,
    Project,
    Requirement,
    RequirementItem,
    Organisation,
    ObjectAssignment,
    Task,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json, uuid, re


GDPR_SEARCH = {
    "customer": Customer.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("customer_id"),
        label=Concat(
            F("customer_first_name"),
            Value(" "),
            F("customer_last_name"),
            Value(" - "),
            F("customer_id"),
            Value(" - "),
            F("organisation_id__organisation_name"),
            Value(" - Is Soft Deleted - "),
            F("is_deleted"),
            output_field=django.db.models.CharField()
        ),
    ).values(
        "label",
        "value",
    ),
    "organisation": Organisation.objects.filter(
        is_deleted=False,
    ).annotate(
        value=F("organisation_id"),
        label=Concat(
            F("organisation_name"),
            Value(" - "),
            F("organisation_id"),
            output_field=django.db.models.CharField()
        ),
    ).values(
        "label",
        "value",
    ),
    "user": User.objects.all().annotate(
        value=F("id"),
        label=Concat(
            F("username"),
            Value(" - "),
            F("first_name"),
            Value(" "),
            F("last_name"),
            Value(" - "),
            F("email"),
            output_field=django.db.models.CharField()
        ),
    ).values(
        "label",
        "value",
    ),
}


# Interal Function
def _delete_customer_data(gdpr_object_id, form: GdprObjectSubmitForm):
    # Flat pack
    project = form.cleaned_data["project"]
    requirement = form.cleaned_data["requirement"]
    requirement_item = form.cleaned_data["requirement_item"]
    task = form.cleaned_data["task"]

    # Get customer data
    customer_data = Customer.objects.get(
        customer_id=gdpr_object_id,
    )
    first_name = customer_data.customer_first_name
    last_name = customer_data.customer_last_name
    email = customer_data.customer_email

    for single_project in project:
        generated_uuid = uuid.uuid4()
        single_project.project_name = re.sub(first_name, str(generated_uuid), single_project.project_name, flags=re.IGNORECASE)
        single_project.project_name = re.sub(last_name, str(generated_uuid), single_project.project_name, flags=re.IGNORECASE)
        single_project.project_name = re.sub(email, str(generated_uuid), single_project.project_name, flags=re.IGNORECASE)
        single_project.project_description = re.sub(first_name, str(generated_uuid), single_project.project_description, flags=re.IGNORECASE)
        single_project.project_description = re.sub(last_name, str(generated_uuid), single_project.project_description, flags=re.IGNORECASE)
        single_project.project_description = re.sub(email, str(generated_uuid), single_project.project_description, flags=re.IGNORECASE)

        single_project.save()

    for single_requirement in requirement:
        generated_uuid = uuid.uuid4()
        single_requirement.requirement_title = re.sub(first_name, str(generated_uuid), single_requirement.requirement_title, flags=re.IGNORECASE)
        single_requirement.requirement_title = re.sub(last_name, str(generated_uuid), single_requirement.requirement_title, flags=re.IGNORECASE)
        single_requirement.requirement_title = re.sub(email, str(generated_uuid), single_requirement.requirement_title, flags=re.IGNORECASE)
        single_requirement.requirement_scope = re.sub(first_name, str(generated_uuid), single_requirement.requirement_scope, flags=re.IGNORECASE)
        single_requirement.requirement_scope = re.sub(last_name, str(generated_uuid), single_requirement.requirement_scope, flags=re.IGNORECASE)
        single_requirement.requirement_scope = re.sub(email, str(generated_uuid), single_requirement.requirement_scope, flags=re.IGNORECASE)

    for single_requirement_item in requirement_item:
        generated_uuid = uuid.uuid4()
        single_requirement_item.requirement_item_title = re.sub(first_name, str(generated_uuid), single_requirement_item.requirement_item_title, flags=re.IGNORECASE)
        single_requirement_item.requirement_item_title = re.sub(last_name, str(generated_uuid), single_requirement_item.requirement_item_title, flags=re.IGNORECASE)
        single_requirement_item.requirement_item_title = re.sub(email, str(generated_uuid), single_requirement_item.requirement_item_title, flags=re.IGNORECASE)
        single_requirement_item.requirement_item_scope = re.sub(first_name, str(generated_uuid), single_requirement_item.requirement_item_scope, flags=re.IGNORECASE)
        single_requirement_item.requirement_item_scope = re.sub(last_name, str(generated_uuid), single_requirement_item.requirement_item_scope, flags=re.IGNORECASE)
        single_requirement_item.requirement_item_scope = re.sub(email, str(generated_uuid), single_requirement_item.requirement_item_scope, flags=re.IGNORECASE)

    for single_task in task:
        generated_uuid = uuid.uuid4()
        single_task.task_short_description = re.sub(first_name, str(generated_uuid), single_task.task_short_description, flags=re.IGNORECASE)
        single_task.task_short_description = re.sub(last_name, str(generated_uuid), single_task.task_short_description, flags=re.IGNORECASE)
        single_task.task_short_description = re.sub(email, str(generated_uuid), single_task.task_short_description, flags=re.IGNORECASE)
        single_task.task_long_description = re.sub(first_name, str(generated_uuid), single_task.task_long_description, flags=re.IGNORECASE)
        single_task.task_long_description = re.sub(last_name, str(generated_uuid), single_task.task_long_description, flags=re.IGNORECASE)
        single_task.task_long_description = re.sub(email, str(generated_uuid), single_task.task_long_description, flags=re.IGNORECASE)

    # Delete the object assignment
    ObjectAssignment.objects.filter(
        customer_id=gdpr_object_id,
    ).delete()

    # Delete the customer
    Customer.objects.get(
        customer_id=gdpr_object_id,
    ).delete()

    return


# Internal Function
def _delete_organisation_data(gdpr_object_id):
    Organisation.objects.get(
        organisation_id=gdpr_object_id,
    ).delete()

    return


# Internal Function
def _delete_user_data(gdpr_object_id, request):
    # Remove all Object Associations first
    ObjectAssignment.objects.filter(
        assigned_user_id=gdpr_object_id,
    ).delete()

    # Go through each table in NearBeach and for the creation/change user - change to current user
    nearbeach_tables = apps.get_app_config("NearBeach").get_models()
    for single_table in nearbeach_tables:
        condition_1 = hasattr(single_table, "change_user")
        condition_2 = hasattr(single_table, "creation_user")
        
        if condition_1 & condition_2:
            single_table.objects.filter(
                Q(
                    change_user_id=gdpr_object_id,
                ) |
                Q(
                    creation_user=gdpr_object_id,
                )
            ).update(
                change_user=request.user,
                creation_user=request.user,
            )
        elif condition_1:
            single_table.objects.filter(
                change_user_id=gdpr_object_id,
            ).update(
                change_user=request.user,
            )
        elif condition_2:
            single_table.objects.filter(
                creation_user_id=gdpr_object_id,
            ).update(
                creation_user=request.user,
            )

    return


# Internal Function
def _get_customer_data(gdpr_object_id):
    """
    User Action Required
    ~~~~~~~~~~~~~~~~~~~~
    Look at ALL objects associated with the customer's organisation. Within objects search for;
    - First name
    - Last name
    - Email
    These will be presented to the front end user as POTENTIAL changes.

    Data To Be Removed
    ~~~~~~~~~~~~~~~~~~
    Look at ALL objects that the customer has been assigned too
    """
    customer_results = get_object_or_404(Customer, pk=gdpr_object_id)
    object_assignment_results = ObjectAssignment.objects.filter(
        customer_id=gdpr_object_id,
    )

    # Flat Pack
    first_name = customer_results.customer_first_name
    last_name = customer_results.customer_last_name
    email = customer_results.customer_email

    object_list = [
        {
            "type": "project",
            "object": Project.objects.filter(
                organisation_id=customer_results.organisation_id,
            ),
            "object_id": "project_id",
            "object_status": "project_status__project_status",
            "object_title": "project_name",
            "fields": [
                "project_name",
                "project_description",
            ],
        },
        {
            "type": "requirement",
            "object": Requirement.objects.filter(
                organisation_id=customer_results.organisation_id,
            ),
            "object_id": "requirement_id",
            "object_status": "requirement_status__requirement_status",
            "object_title": "requirement_title",
            "fields": [
                "requirement_title",
                "requirement_scope",
            ],
        },
        {
            "type": "requirement_item",
            "object": RequirementItem.objects.filter(
                requirement_id__in=Requirement.objects.filter(
                    organisation_id=customer_results.organisation_id,
                ).values("requirement_id"),
            ),
            "object_id": "requirement_item_id",
            "object_status": "requirement_item_status__requirement_item_status",
            "object_title": "requirement_item_title",
            "fields": [
                "requirement_item_title",
                "requirement_item_scope",
            ],
        },
        {
            "type": "task",
            "object": Task.objects.filter(
                organisation_id=customer_results.organisation_id,
            ),
            "object_id": "task_id",
            "object_status": "task_status__task_status",
            "object_title": "task_short_description",
            "fields": [
                "task_short_description",
                "task_long_description",
            ],
        },
    ]

    user_action_required = {}
    data_to_be_deleted = {}
    for object in object_list:
        # Gather the variables
        type = object["type"]
        object_id = object["object_id"]
        object_status = object["object_status"]
        object_title = object["object_title"]
        empty_queryset = object["object"].none()

        # Loop through the fields to get the user_action_required
        for object_field in object["fields"]:
            # Store the data against the type
            empty_queryset = empty_queryset | object["object"].filter(
                Q(
                    **{F"{object_field}__icontains": first_name}
                ) |
                Q(
                    **{F"{object_field}__icontains": last_name}
                ) |
                Q(
                    **{F"{object_field}__icontains": email}
                )
            ).annotate(
                object_id=F(object_id),
                object_status=F(object_status),
                object_title=F(object_title),
            ).values(
                "pk",
                "object_id",
                "object_status",
                "object_title",
            )

        # Convert the json to a string, and then back into json format
        empty_queryset = json.dumps(list(empty_queryset), cls=DjangoJSONEncoder)
        user_action_required[type] = json.loads(empty_queryset)

        # Process data to be deleted
        delete_data = object_assignment_results.filter(
            **{F"{object_id}__isnull": False},
        ).annotate(
            object_id=F(object_id),
            object_title=F(F"{object_id}__{object_title}"),
            object_status=F(F"{object_id}__{object_status}"),
        ).values(
            "pk",
            "object_id",
            "object_title",
            "object_status",
        )

        delete_data = json.dumps(list(delete_data), cls=DjangoJSONEncoder)
        data_to_be_deleted[type] = json.loads(delete_data)

    return {
        "user_action_required": user_action_required,
        "data_to_be_deleted": data_to_be_deleted,
    }


# Internal Function
def _get_organisation_data(gdpr_object_id):
    object_list = [
        {
            "type": "project",
            "object": Project.objects.filter(
                organisation_id=gdpr_object_id,
            ),
            "object_id": "project_id",
            "object_status": "project_status__project_status",
            "object_title": "project_name",
        },
        {
            "type": "requirement",
            "object": Requirement.objects.filter(
                organisation_id=gdpr_object_id,
            ),
            "object_id": "requirement_id",
            "object_status": "requirement_status__requirement_status",
            "object_title": "requirement_title",
        },
        {
            "type": "requirement_item",
            "object": RequirementItem.objects.filter(
                requirement_id__in=Requirement.objects.filter(
                    organisation_id=gdpr_object_id,
                ).values("requirement_id"),
            ),
            "object_id": "requirement_item_id",
            "object_status": "requirement_item_status__requirement_item_status",
            "object_title": "requirement_item_scope",
        },
        {
            "type": "task",
            "object": Task.objects.filter(
                organisation_id=gdpr_object_id,
            ),
            "object_id": "task_id",
            "object_status": "task_status__task_status",
            "object_title": "task_short_description",
        }
    ]

    # Loop through object data and construct the data required
    user_action_required = {}
    data_to_be_deleted = {}
    for object in object_list:
        # Gather the variables
        type = object["type"]
        object_id = object["object_id"]
        object_status = object["object_status"]
        object_title = object["object_title"]
        empty_queryset = object["object"].none()

        # Process the data to be deleted
        delete_data = object["object"].annotate(
            object_id=F(object_id),
            object_title=F(object_title),
            object_status=F(object_status),
        ).values(
            "pk",
            "object_id",
            "object_title",
            "object_status",
        )

        delete_data = json.dumps(list(delete_data), cls=DjangoJSONEncoder)
        data_to_be_deleted[type] = json.loads(delete_data)

    return {
        "user_action_required": user_action_required,
        "data_to_be_deleted": data_to_be_deleted,
    }


# Internal Function
def _get_user_data(gdpr_object_id):
    user_results = User.objects.get(
        id=gdpr_object_id,
    )
    object_assignment_results = ObjectAssignment.objects.filter(
        Q(
            change_user_id=gdpr_object_id,
        ) |
        Q(
            assigned_user_id=gdpr_object_id,
        )
    )

    # Flat pack
    first_name = user_results.first_name
    last_name = user_results.last_name
    email = user_results.email

    object_list = [
        {
            "type": "project",
            "object": Project.objects.filter(
                Q(
                    change_user_id=gdpr_object_id,
                ) |
                Q(
                    creation_user_id=gdpr_object_id,
                )
            ),
            "object_id": "project_id",
            "object_status": "project_status__project_status",
            "object_title": "project_name",
            "fields": [
                "project_name",
                "project_description",
            ],
        },
        {
            "type": "requirement",
            "object": Requirement.objects.filter(
                Q(
                    change_user_id=gdpr_object_id,
                ) |
                Q(
                    creation_user_id=gdpr_object_id,
                )
            ),
            "object_id": "requirement_id",
            "object_status": "requirement_status__requirement_status",
            "object_title": "requirement_title",
            "fields": [
                "requirement_title",
                "requirement_scope",
            ],
        },
        {
            "type": "requirement_item",
            "object": RequirementItem.objects.filter(
                Q(
                    change_user_id=gdpr_object_id,
                )
            ),
            "object_id": "requirement_item_id",
            "object_status": "requirement_item_status__requirement_item_status",
            "object_title": "requirement_item_scope",
            "fields": [
                "requirement_item_title",
                "requirement_item_scope",
            ],
        },
        {
            "type": "task",
            "object": Task.objects.filter(
                Q(
                    change_user_id=gdpr_object_id,
                ) |
                Q(
                    creation_user_id=gdpr_object_id,
                )
            ),
            "object_id": "task_id",
            "object_status": "task_status__task_status",
            "object_title": "task_short_description",
            "fields": [
                "task_short_description",
                "task_long_description",
            ],
        },
    ]

    user_action_required = {}
    data_to_be_deleted = {}
    for object in object_list:
        # Gather the variables
        type = object["type"]
        object_id = object["object_id"]
        object_status = object["object_status"]
        object_title = object["object_title"]
        empty_queryset = object["object"].none()

        # Loop through the fields to get the user_action_required
        for object_field in object["fields"]:
            # Store the data against the type
            empty_queryset = empty_queryset | object["object"].filter(
                Q(
                    **{F"{object_field}__icontains": first_name}
                ) |
                Q(
                    **{F"{object_field}__icontains": last_name}
                ) |
                Q(
                    **{F"{object_field}__icontains": email}
                )
            ).annotate(
                object_id=F(object_id),
                object_status=F(object_status),
                object_title=F(object_title),
            ).values(
                "pk",
                "object_id",
                "object_status",
                "object_title",
            )

        # Convert the json to a string, and then back into json format
        empty_queryset = json.dumps(list(empty_queryset), cls=DjangoJSONEncoder)
        user_action_required[type] = json.loads(empty_queryset)

        # Process data to be deleted
        delete_data = object_assignment_results.filter(
            **{F"{object_id}__isnull": False},
        ).annotate(
            object_id=F(object_id),
            object_title=F(F"{object_id}__{object_title}"),
            object_status=F(F"{object_id}__{object_status}"),
        ).values(
            "pk",
            "object_id",
            "object_title",
            "object_status",
        )

        delete_data = json.dumps(list(delete_data), cls=DjangoJSONEncoder)
        data_to_be_deleted[type] = json.loads(delete_data)

    return {
        "user_action_required": user_action_required,
        "data_to_be_deleted": data_to_be_deleted,
    }


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def gdpr_get_data(request):
    form = GdprDataRequestForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Dependent on the GDPR Type, depends where we fetch the data
    gdpr_object_type = form.cleaned_data["gdpr_object_type"]
    gdpr_object_id = form.cleaned_data["gdpr_object_id"]
    if gdpr_object_type == "customer":
        results = _get_customer_data(gdpr_object_id)
    elif gdpr_object_type == "organisation":
        results = _get_organisation_data(gdpr_object_id)
    elif gdpr_object_type == "user":
        # in the odd case a user picks themselfs to delete, send back an error
        if request.user.pk == gdpr_object_id:
            return HttpResponseBadRequest("Don't delete yourself!")

        results = _get_user_data(gdpr_object_id)
    else:
        return HttpResponseBadRequest("GDPR Object Type does not exist")

    # Check to see if results is None, if so there has been an error
    if results is None:
        return HttpResponseBadRequest("GDPR Object Type and Object Id do not exist")

    # Convert the results to JSON and send back to user
    results = json.dumps(results, cls=DjangoJSONEncoder)

    return JsonResponse(json.loads(results), safe=False)


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def gdpr_search_data(request):
    form = GdprObjectTypeForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the results
    gdpr_object_type = form.cleaned_data["gdpr_object_type"]
    results = GDPR_SEARCH[
        gdpr_object_type
    ]

    # Stop the user from picking themselfs to delete - as it will cause many issues
    if gdpr_object_type == "user":
        results = results.exclude(username=request.user)

    # Convert the results
    return HttpResponse(
        json.dumps(list(results), cls=DjangoJSONEncoder),
        content_type="application/json",
    )


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def gdpr_submit(request):
    form = GdprObjectSubmitForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    gdpr_object_type = form.cleaned_data["gdpr_object_type"]
    gdpr_object_id = form.cleaned_data["gdpr_object_id"]
    if gdpr_object_type == "customer":
        _delete_customer_data(gdpr_object_id, form)
    elif gdpr_object_type == "organisation":
        _delete_organisation_data(gdpr_object_id)
    elif gdpr_object_type == "user":
        _delete_user_data(gdpr_object_id, request)
    else:
        return HttpResponseBadRequest("Object Type Not Found")

    return HttpResponse(F"{gdpr_object_type} has been deleted")


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def gdpr_wizard(request):
    # Get template
    t = get_template("NearBeach/gdpr/gdpr_wizard.html")

    # Get context
    c = {
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))
