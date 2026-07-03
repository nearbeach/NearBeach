from NearBeach.models import (
    Group,
    KanbanCard,
    ObjectAssignment,
    UserGroup,
)
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.serializers.group_serializer import GroupSerializer
from django.db.models import F
from django.contrib.auth.models import User

from serializers.group_and_user_serializer import GroupAndUserSerializer


class GroupService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete groups against an object"""
    def _get_group_list(self):
        object_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
        )

        # If the destination is NOT a kanban_card - we'll send back the filtered results
        if self.destination != "kanban_card":
            return object_results.filter(
                **{F"{self.destination}_id": self.location_id},
            )

        # We need to get the kanban card's kanban board's id
        kanban_card_results = KanbanCard.objects.get(kanban_card_id=self.location_id)

        return object_results.filter(
            kanban_board_id=kanban_card_results.kanban_board_id,
        )

    def _get_potential_user_list(self):
        # Get a list of users we want to exclude
        object_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            assigned_user_id__isnull=False,
            **{F"{self.destination}_id": self.location_id},
        )

        # Get a list of all the groups associated with this destination
        group_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
        )

        if self.destination != "kanban_card":
            group_results = group_results.filter(
                **{F"{self.destination}_id": self.location_id},
            )
        else:
            # Get the kanban board information from the card
            kanban_card_results = KanbanCard.objects.get(kanban_card_id=self.location_id)

            group_results = group_results.filter(
                kanban_board_id=kanban_card_results.kanban_board_id,
            )

        # Get a list of users who are associated with these groups & not in the excluded list
        return User.objects.filter(
            id__in=UserGroup.objects.filter(
                is_deleted=False,
                group_id__in=group_results.values("group_id"),
            ).values("username_id"),
            is_active=True,
        ).exclude(
            id__in=object_results.values("assigned_user_id")
        ).annotate(
            profile_picture=F('userprofilepicture__document_id__document_key')
        )

    @staticmethod
    def _get_user_list(destination, location_id):
        # Get the data we want
        object_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            assigned_user_id__isnull=False,
            **{F"{destination}_id": location_id}
        ).annotate(
            profile_picture=F("assigned_user_id__userprofilepicture__document_id__document_key")
        )

        return object_results

    def create(self, request):
        # Serialize the data for references
        serializer = GroupSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer, False

        # Flat pack the variables
        # group_list = serializer.data["group_list"]
        # user_list = serializer.data["user_list"]

        # Loop through all the groups and add to the current object
        for single_group in group_list:
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

        # Get the current permission/groups for this object
        object_groups = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
            **{F"{destination}_id": location_id},
        ).values('group_id')
        error_array = []

        return_data = self._get_group_and_user_list(
            destination,
            location_id,
            request,
        )

        if len(error_array) > 0:
            return Response(
                data={
                    "error_array": error_array,
                    "error_message": "Users in Error Array can not be added to object, as their groups are not assigned to object",
                    "error_note": "Please run the get command to get the latest groups and users list",
                }
            )

        # TODO - 0.32 - Look at the obtaining the object_assignment_id from the database, so users can easily delete both users and groups from the object
        return Response(
            data=return_data.data,
            status=status.HTTP_201_CREATED,
        )
        pass

    def delete(self, request, object_id):
        pass



    def get_list(self, request):
        # Get the data dependent on the object lookup
        group_list = self._get_group_list
        user_list = self._get_user_list
        potential_user_list = self._get_potential_user_list

        return GroupAndUserSerializer(
            data={
                "group_list": group_list,
                "potential_user_list": potential_user_list,
                "user_list": user_list,
            }
        )

    def update(self, request, object_id):
        pass
