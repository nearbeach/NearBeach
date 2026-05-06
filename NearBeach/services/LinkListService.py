from NearBeach.models import (
    ObjectAssignment,
    KanbanCard,
)
from django.db.models import Q, F, Value

from NearBeach.serializers.object_data.link_serializer import LinkSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction, OBJECT_STRUCTURE
from NearBeach.utils.dicts.relation_dict import RELATION_DICT


class LinkListService(ObjectServiceAbstraction):
    """Service to help list/add/delete object links"""
    def _get_parent_link(self, serializer: LinkSerializer):
        """Uses data to determine the parent object"""
        object_type = serializer.validated_data["object_type"]

        # If object_type == destination, we'll change this to meta
        object_type = "meta_object" if object_type == self.destination else object_type

        # Fetch relationship
        relationship = serializer.validated_data["object_relation"]

        # If relationship in array - then object type will be parent object
        return str(object_type) if relationship in ["blocked_by", "sub_object_of", "has_duplicate"] else str(self.destination)

    def _set_meta_object(self, object_assignment: ObjectAssignment, single_object, object_type: str):
        # If object destination is the same as the object type, add the meta_object value
        if self.destination == object_type:
            # We need to set the metaobject
            setattr(object_assignment, "meta_object", single_object.pk)

            # Update the status and the title with the correct data
            setattr(
                object_assignment,
                "meta_object_title",
                getattr(single_object, "title"),
            )

            setattr(
                object_assignment,
                "meta_object_status",
                getattr(single_object, "status"),
            )

        return object_assignment

    def create(self, request):
        serializer = LinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer, False

        # Get the parent object of
        object_type = serializer.validated_data["object_type"]
        object_relation = serializer.validated_data["object_relation"]

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
            parent_link=self._get_parent_link(serializer),
            link_relationship=RELATION_DICT[object_relation],
        )

        # Set meta object
        submit_object_assignment = self._set_meta_object(submit_object_assignment, single_object, object_type)

        # Save
        submit_object_assignment.save()

        # Serializer
        serializer = LinkSerializer(submit_object_assignment, many=False)

        # Now get the new data
        return serializer, True

    def delete(self, object_id):
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            pk=object_id,
            **{self.destination: self.location_id},
        )

        # If there are no values to update - notify the user
        if len(object_assignment_results) == 0:
            return False

        # Soft delete the data
        object_assignment_results.update(is_deleted=True)

        return True

    def get_list(self, _):
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

        # Set up the data point list to loop through. Have to add the generic meta
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

    def update(self, request, object_assignment_id):
        """Method to update a link"""
        serializer = LinkSerializer(
            data=request.data,
        )
        if not serializer.is_valid():
            return serializer.errors, False

        # Fetch object assignment row
        object_assignment = ObjectAssignment.objects.get(
            Q(
                is_deleted=False,
                pk=object_assignment_id,
            ) &
            Q(
                # The object could be in its natural field, or the meta field
                Q(
                    **{self.destination + "_id": self.location_id},
                ) |
                Q(
                    meta_object=self.location_id,
                )
            )
        )
        if object_assignment is None:
            return {"Object Assignment does not exist"}, False

        # Get the parent object of
        object_id = serializer.validated_data["object_id"]
        object_type = serializer.validated_data["object_type"]
        object_relation = serializer.validated_data["object_relation"]

        # Check to make sure the object_id exists
        if not object_type in list(self.object_dict):
            return {"Object Type not in system"}, False

        # Get single object
        single_object = self.object_dict[object_type].get(pk=object_id)
        link_relationship = RELATION_DICT[object_relation]
        parent_link=self._get_parent_link(serializer)

        # Update the data
        setattr(object_assignment, object_type, single_object)
        setattr(object_assignment, F"{self.destination}_id", int(self.location_id))
        object_assignment.change_user = request.user
        object_assignment.parent_link=str(parent_link)
        object_assignment.link_relationship=str(link_relationship)

        # Handle meta
        object_assignment = self._set_meta_object(object_assignment, single_object, object_type)

        # Save
        object_assignment.save()

        # Now get the new data
        return None, True
