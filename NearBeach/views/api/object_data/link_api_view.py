from collections import namedtuple

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, F, Value
from NearBeach.decorators.check_user_permissions.api_object_data_permissions_v0 import api_object_data_permissions
from NearBeach.serializers.object_data.link_serializer import LinkSerializer
from NearBeach.models import (
    ChangeTask,
    KanbanCard,
    ObjectAssignment,
    Project,
    Requirement,
    RequirementItem,
    Task,
)
from NearBeach.views.tools.internal_functions import set_object_from_destination

OBJECT_STRUCTURE = namedtuple(
    "ObjectStructure",
    [
        "object_id",
        "object_title",
        "object_status",
        "object_type",
        "non_null_field"
    ]
)

OBJECT_DICT = {
    "change_task": ChangeTask.objects,
    "project": Project.objects,
    "task": Task.objects,
    "requirement": Requirement.objects,
    "requirement_item": RequirementItem.objects,
}

RELATION_DICT = {
    "relates": "Relate",
    "blocked_by": "Block",
    "blocking": "Block",
    "sub_object_of": "Subobject",
    "parent_object_of": "Subobject",
    "has_duplicate": "Duplicate",
    "duplicate_object": "Duplicate",
}

OBJECT_TITLE = {
    "change_task": "change_task_title",
    "project": "project_name",
    "task": "task_short_description",
    "requirement": "requirement_title",
    "requirement_item": "requirement_item_title",
}


@extend_schema(
    tags=["Object Data|Link"]
)
class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def _get_list(self, destination, location_id):
        # Check objects that match the destination and location id
        # Also make sure we get any meta data where the destination is not null
        object_assignment_results = ObjectAssignment.objects.filter(
            Q(
                is_deleted=False,
            ) &
            Q(
                Q(
                    # Where destination and location id match
                    **{destination: location_id},
                )
                | Q(
                    **{destination + "__isnull": False},
                    meta_object=location_id,
                )
            )
        )

        # Setup the data point list to loop through. Have to add the generic meta
        data_point_list: list[OBJECT_STRUCTURE] = [
            OBJECT_STRUCTURE(
                "project_id",
                "project_id__project_name",
                "project_id__project_status__project_status",
                "project",
                "project"
            ),
            OBJECT_STRUCTURE(
                "task_id",
                "task_id__task_short_description",
                "task_id__task_status__task_status",
                "task",
                "task"
            ),
            OBJECT_STRUCTURE(
                "requirement_id",
                "requirement_id__requirement_title",
                "requirement_id__requirement_status__requirement_status",
                "requirement",
                "requirement"
            ),
            OBJECT_STRUCTURE(
                "requirement_item_id",
                "requirement_item_id__requirement_item_title",
                "requirement_item_id__requirement_item_status__requirement_item_status",
                "requirement_item",
                "requirement_item"
            ),
            OBJECT_STRUCTURE(
                "meta_object",
                "meta_object_title",
                "meta_object_status",
                destination,
                "meta_object"
            ),
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
                    object_type=Value(data_point.object_type),
                    reverse_relation=Value(True),
                ).values(
                    "object_assignment_id",
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
                    object_type=Value(data_point.object_type),
                    reverse_relation=Value(False),
                ).values(
                    "object_assignment_id",
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
                **{destination + "_id": location_id},
                is_archived=False,
            ).annotate(
                object_assignment_id=Value("0"),
                object_id=F("kanban_card_id"),
                object_title=F("kanban_card_text"),
                object_status=F("kanban_column_id__kanban_column_name"),
                object_type=Value("card"),
                reverse_relation=Value(False),
                link_relationship=Value("Card"),
                parent_link=Value("card"),
            ).values(
                "object_assignment_id",
                "object_id",
                "object_title",
                "object_status",
                "object_type",
                "link_relationship",
                "parent_link",
                "reverse_relation",
            ))

        # Return the serialized data
        return LinkSerializer(
            data_results,
            many=True,
        )

    @api_object_data_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = LinkSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the parent object of
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]
        object_relation = serializer.data["object_relation"]

        # Loop through the results and add them in.
        # We will loop through each object type, and add them in accordinly
        for object_type in list(OBJECT_DICT.keys()):
            # Get the results of each object type and add them
            for row in request.POST.getlist(object_type):
                single_object = OBJECT_DICT[object_type].get(pk=row)

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
                submit_object_assignment.link_relationship = RELATION_DICT[object_relation]

                # If object destination is the same as the object type, add the meta_object value
                if destination == object_type:
                    # We need to set the meta object
                    setattr(submit_object_assignment, "meta_object", row)

                    # Update the status and the title with the correct data
                    setattr(
                        submit_object_assignment,
                        "meta_object_title",
                        getattr(single_object, OBJECT_TITLE[object_type]),
                    )

                    setattr(
                        submit_object_assignment,
                        "meta_object_status",
                        getattr(single_object, F"{object_type}_status"),
                    )

                submit_object_assignment.save()

        # Now get the new data
        serializer = self._get_list(destination, location_id)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @api_object_data_permissions(min_permission_level=4)
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get data from serializer
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the object we wish to remove
        remove_object = ObjectAssignment.objects.filter(
            **{F"{destination}_id": location_id},
            is_deleted=False,
            object_assignment_id=pk,
        )

        # Check to make sure we have data
        if len(remove_object) == 0:
            return Response(
                data={'Link does not exist'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Delete the data
        remove_object.update(
            is_deleted=True,
            change_user=request.user
        )

        # Now get the new data
        serializer = self._get_list(destination, location_id)
        return Response(
            data=serializer.data,
            status=status.HTTP_204_NO_CONTENT
        )

    @api_object_data_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        destination = kwargs["destination"]
        location_id = kwargs["location_id"]

        # Get the serialized data
        serializer = self._get_list(destination, location_id)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
