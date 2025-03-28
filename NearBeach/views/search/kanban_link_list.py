from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F
from django.conf import settings
from NearBeach.forms import SearchObjectsForm
from NearBeach.models import (
    ObjectAssignment,
    Project,
    Requirement,
    RequirementItem,
    Task,
    UserGroup,
)
import json
import math

# Define global variables
SEARCH_PAGE_SIZE = getattr(settings, 'SEARCH_PAGE_SIZE', 5)


class KanbanLinkList:
    OBJECT_SETUP = {
        "project": {
            "fields": {
                "id": "project_id",
                "title": "project_name",
                "status": "project_status__project_status",
            },
            "objects": Project.objects,
            "title": "project_name",
        },
        "task": {
            "fields": {
                "id": "task_id",
                "title": "task_short_description",
                "status": "task_status__task_status",
            },
            "objects": Task.objects,
            "title": "task_short_description",
        },
        "requirement": {
            "fields": {
                "id": "requirement_id",
                "title": "requirement_title",
                "status": "requirement_status__requirement_status",
            },
            "objects": Requirement.objects,
            "title": "requirement_title",
        },
        "requirement_item": {
            "fields": {
                "id": "requirement_item_id",
                "title": "requirement_item_title",
                "status": "requirement_item_status__requirement_item_status",
            },
            "objects": RequirementItem.objects,
            "title": "requirement_item_title",
        },
    }

    results = {}

    def __init__(self, form: SearchObjectsForm, request):
        # Create an empty object to fill
        return_results = {}

        for single_object in form.cleaned_data['array_of_objects']:
            # Get the results from the method
            result, count = self._get_single_search_object(form, single_object, request)

            # Check to make sure we are not getting None
            if result is not None:
                result = json.dumps(list(result), cls=DjangoJSONEncoder)
                return_results[single_object] = json.loads(result)
                return_results[F"{single_object}_number_of_pages"] = math.ceil(count / SEARCH_PAGE_SIZE)
                return_results[F"{single_object}_current_page"] = form.cleaned_data["destination_page"]

        self.results = return_results

    def _get_single_search_object(self, form: SearchObjectsForm, object_name, request):
        # Check to make sure we can search for this object
        if object_name not in self.OBJECT_SETUP:
            return None

        # shortcut variable
        id_field = self._get_id_name(object_name)

        # Used to shorten the code below
        data = self.OBJECT_SETUP[object_name]

        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
            is_deleted=False,
                username=request.user,
            ).values("group_id"),
        )

        results = data["objects"].filter(
            is_deleted=False,
            **{F"{id_field}__in": object_assignment_results.filter(
                **{F"{id_field}__isnull": False}
            ).values(F"{id_field}")}
        ).exclude(
            **{F"{object_name}_status__{object_name}_higher_order_status": "Closed"},
        ).annotate(
            id=F(data["fields"]["id"]),
            title=F(data["fields"]["title"]),
            status=F(data["fields"]["status"]),
        ).values(
            "id",
            "title",
            "status",
        )

        # Split the space results - then apply the filter of each split value
        for split_row in form.cleaned_data["search"].split(" "):
            # If split row is a number, search both the title and object id
            if split_row.isnumeric():
                results = results.filter(
                    Q(
                        **{F"{data['title']}__icontains": split_row}
                    ) | Q(
                        **{F"{self._get_id_name(object_name)}": split_row}
                    )
                )
            else:
                results = results.filter(
                    Q(
                        **{F"{data['title']}__icontains": split_row}
                    )
                )

        # EXCLUSION OF RESULTS
        # There are some requests that come through that need to be
        # excluded
        exclude_destination = form.cleaned_data["exclude_destination"]
        exclude_location_id = form.cleaned_data["exclude_location_id"]
        if exclude_destination and exclude_location_id:
            # shortcut variable
            id_field = self._get_id_name(object_name)

            results = results.exclude(
                **{F"{id_field}__in": ObjectAssignment.objects.filter(
                    is_deleted=False,
                    **{F"{object_name}_id__isnull": False},
                    **{F"{exclude_destination}_id": exclude_location_id},
                ).values(F"{object_name}_id")}
            )

        # Pagination :D
        destination_page = form.cleaned_data["destination_page"]

        # Apply the shift of the destination page, as we should -1 the value. Due to the front end sending the actual
        # page number
        destination_page = 0 if destination_page <= 0 else destination_page - 1

        # Return the results, and length of the complete data set
        return results[destination_page * SEARCH_PAGE_SIZE:(destination_page + 1) * SEARCH_PAGE_SIZE], len(results)

    @staticmethod
    def _get_id_name(object_name):
        if object_name == "request_for_change":
            return "rfc_id"

        return F"{object_name}_id"
