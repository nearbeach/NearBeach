from collections import namedtuple
from NearBeach.models import (
    ObjectAssignment,
    KanbanCard,
    ChangeTask,
    Project,
    Task,
    Requirement,
    RequirementItem,
)
from django.db.models import Q, F, Value

from NearBeach.serializers.object_data.link_serializer import LinkSerializer
from NearBeach.utils.dicts.relation_dict import RELATION_DICT

# OBJECT STRUCTURE TYPE
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


class LinkListService():
    """Service to help list/add/delete object links"""
    object_dict = {
        "change_task": ChangeTask.objects,
        "project": Project.objects,
        "task": Task.objects,
        "requirement": Requirement.objects,
        "requirement_item": RequirementItem.objects,
    }

    def __init__(self, destination: str, location_id: int):
        """Initialise the class"""
        self.destination = destination
        self.location_id = location_id

    def create_link(self, request):
        serializer = LinkSerializer(
            data=request.data,
            # context={'request': request}
        )
        if not serializer.is_valid():
            return serializer, False

        # Get the parent object of
        object_type = serializer.data["object_type"]
        object_relation = serializer.data["object_relation"]

        # Check to make sure the object_id exists
        if not object_type in list(self.object_dict):
            return {"Object Type not in system"}, False

        # We have the object type
        # We have the object id
        single_object = self.object_dict[object_type].get(pk=serializer.validated_data["object_id"])

        submit_object_assignment = ObjectAssignment(
            change_user=request.user,
            **{object_type: single_object},
            **{F"{self.destination}_id": self.location_id},
        )

        if object_relation in ['relates', 'blocking', 'parent_object_of', 'has_duplicate']:
            submit_object_assignment.parent_link = self.destination
        else:
            if self.destination == object_type:
                submit_object_assignment.parent_link = "meta_object"
            else:
                submit_object_assignment.parent_link = object_type

        # Add the link relationship from the dictionary
        submit_object_assignment.link_relationship = RELATION_DICT[object_relation]

        # If object destination is the same as the object type, add the meta_object value
        if self.destination == object_type:
            # We need to set the meta object
            setattr(submit_object_assignment, "meta_object", object_type)

            # Update the status and the title with the correct data
            setattr(
                submit_object_assignment,
                "meta_object_title",
                getattr(single_object, "title"),
            )

            setattr(
                submit_object_assignment,
                "meta_object_status",
                getattr(single_object, "status"),
            )

        submit_object_assignment.save()

        # Now get the new data
        return self.get_link_list(), True

    def delete_link(self, link_pk):
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            pk=link_pk,
            **{self.destination: self.location_id},
        )

        # If there are no values to update - notify the user
        if len(object_assignment_results) == 0:
            return False

        # Soft delete the data
        object_assignment_results.update(is_deleted=True)

        return True

    def get_link_list(self):
        object_assignment_results = ObjectAssignment.objects.filter(
            Q(
                is_deleted=False,
            ) &
            Q(
                Q(
                    # Where destination and location id match
                    **{self.destination: self.location_id},
                )
                | Q(
                    **{self.destination + "__isnull": False},
                    meta_object=self.location_id,
                )
            )
        )

        # Setup the data point list to loop through. Have to add the generic meta
        data_point_list: list[OBJECT_STRUCTURE] = [
            OBJECT_STRUCTURE(
                "project_id",
                "project__title",
                "project__status__status",
                "project",
                "project"
            ),
            OBJECT_STRUCTURE(
                "task_id",
                "task__title",
                "task__status__status",
                "task",
                "task"
            ),
            OBJECT_STRUCTURE(
                "requirement_id",
                "requirement__title",
                "requirement__status__status",
                "requirement",
                "requirement"
            ),
            OBJECT_STRUCTURE(
                "requirement_item_id",
                "requirement_item__title",
                "requirement_item__status__status",
                "requirement_item",
                "requirement_item"
            ),
            OBJECT_STRUCTURE(
                "meta_object",
                "meta_object_title",
                "meta_object_status",
                self.destination,
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
            if self.destination == data_point.non_null_field:
                data_results.extend(object_assignment_results.filter(
                    meta_object=self.location_id,
                    **{self.destination + "__isnull": False},
                ).annotate(
                    object_assignment_id=F("id"),
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
                    meta_object=self.location_id,
                ).annotate(
                    object_assignment_id=F("id"),
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
        if self.destination in ["project", "task", "requirement"]:
            data_results.extend(KanbanCard.objects.filter(
                # **{data_point.non_null_field + "__isnull": False},
                **{self.destination + "_id": self.location_id},
                is_archived=False,
            ).annotate(
                object_assignment_id=Value("0"),
                object_id=F("id"),
                object_title=F("title"),
                object_status=F("kanban_column__name"),
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
