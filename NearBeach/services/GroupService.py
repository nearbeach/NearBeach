from django.db.models.functions import Concat

from NearBeach.models import (
    Group,
    KanbanCard,
    ObjectAssignment,
    UserGroup,
)
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from django.db.models import F, Value
from django.contrib.auth.models import User

from serializers.group_and_user_serializer import GroupAndUserSerializer
from serializers.group_list_serializer import GroupListSerializer


class GroupService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete groups against an object"""
    def _clean_users_from_object(self):
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
            **{F"{self.destination}_id": self.location_id},
        )

        # Users associated with the groups
        user_list_results = UserGroup.objects.filter(
            is_deleted=False,
            group_id__in=groups_associated.values('group_id'),
        )

        remove_user_list = ObjectAssignment.objects.filter(
            is_deleted=False,
            assigned_user_id__isnull=False,
            **{F"{self.destination}_id": self.location_id},
        ).exclude(
            assigned_user_id__in=user_list_results.values('username_id'),
        )

        # Delete what is left
        remove_user_list.update(
            is_deleted=True,
        )

    def _get_group_list(self):
        object_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__isnull=False,
            **{F"{self.destination}_id": self.location_id},
        )

        # If the destination is NOT a kanban_card - we'll send back the filtered results
        if self.destination != "kanban_card":
            return Group.objects.filter(
                is_deleted=False,
                id__in=object_results.filter(
                    **{F"{self.destination}_id": self.location_id},
                ).values("group_id"),
            )

        # We need to get the kanban card's kanban board's id
        kanban_card_results = KanbanCard.objects.get(kanban_card_id=self.location_id)

        return Group.objects.filter(
            is_deleted=False,
            id__in=object_results.filter(
                kanban_board_id=kanban_card_results.kanban_board_id,
            ).values("group_id"),
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
            profile_picture=F('userprofilepicture__document_id'),
            full_name=Concat('first_name', Value(' '), 'last_name'),
        )

    def _get_user_list(self):
        # Get the data we want
        object_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            assigned_user_id__isnull=False,
            **{F"{self.destination}_id": self.location_id}
        )

        return User.objects.filter(
            id__in=object_results.values("assigned_user_id"),
            is_active=True,
        ).annotate(
            profile_picture=F("userprofilepicture__document_id"),
            full_name=Concat('first_name', Value(' '), 'last_name'),
        )

    def create(self, request):
        # Serialize the data for references
        serializer = GroupListSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer, False

        # Loop through all the groups and add to the current object
        for single_group in serializer.validated_data["group_list"]:
            # Construct the object assignment
            submit_object_assignment = ObjectAssignment(
                group_id=single_group.id,
                change_user=request.user,
                **{F"{self.destination}_id": self.location_id},
            )

            # Save the data
            submit_object_assignment.save()

        return None, True


    def delete(self, request, group_pk):
        remove_object_assignment = ObjectAssignment.objects.filter(
            group_id=group_pk,
            **{F"{self.destination}_id": self.location_id}
        )

        # If there is nothing to delete, notify the user
        if len(remove_object_assignment) == 0:
            return False

        # Remove the group
        remove_object_assignment.update(
            is_deleted=True,
        )

        # Remove any unwanted users
        self._clean_users_from_object()

        return True

    def get_list(self, request):
        # Get the data dependent on the object lookup
        group_list = self._get_group_list()
        user_list = self._get_user_list()
        potential_user_list = self._get_potential_user_list()

        # Data
        data = {
            "group_list": group_list,
            "potential_user_list": potential_user_list,
            "user_list": user_list,
        }

        return GroupAndUserSerializer(data)

    def update(self, request, object_id):
        pass
