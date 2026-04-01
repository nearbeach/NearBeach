from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F

from NearBeach.models import (
    ListOfRequirementStatus,
    ListOfRequirementItemStatus,
    ListOfProjectStatus,
    ListOfTaskStatus,
    UserGroup, ListOfRequirementType, ListOfRequirementItemType, Tag,
)
from NearBeach.serializers.user.user_initial_data_serializer import UserInitialDataSerializer


@extend_schema(
    exclude=True,
)
class UserInitialDataView(APIView):
    """Class dealing with user intial data"""
    serializer_class = None

    @staticmethod
    def _get_permissions(user):
        """Method to get the current user's permissions"""
        return UserGroup.objects.filter(
            is_deleted=False,
            username=user,
            group__is_deleted=False,
            permission_set__is_deleted=False,
        ).values(
            "group_id",
            group_name=F("group__name"),
            administration_assign_user_to_group=F("permission_set__administration_assign_user_to_group"),
            administration_create_group=F("permission_set__administration_create_group"),
            administration_create_permission_set=F("permission_set__administration_create_permission_set"),
            administration_create_user=F("permission_set__administration_create_user"),
            customer=F("permission_set__customer"),
            document=F("permission_set__document"),
            kanban_board=F("permission_set__kanban_board"),
            organisation=F("permission_set__organisation"),
            organisation_note=F("permission_set__organisation_note"),
            project=F("permission_set__project"),
            request_for_change=F("permission_set__request_for_change"),
            requirement=F("permission_set__requirement"),
            requirement_item_note=F("permission_set__requirement_item_note"),
            requirement_note=F("permission_set__requirement_note"),
            schedule_object=F("permission_set__schedule_object"),
            sprint=F("permission_set__sprint"),
            task=F("permission_set__task"),
            tag=F("permission_set__tag"),
            kanban_note=F("permission_set__kanban_note"),
            project_note=F("permission_set__project_note"),
            task_note=F("permission_set__task_note"),
        )

    @staticmethod
    def _get_status():
        return {
            "requirement": ListOfRequirementStatus.objects.filter(
                is_deleted=False,
            ).order_by("sort_order"),
            "requirement_item": ListOfRequirementItemStatus.objects.filter(
                is_deleted=False,
            ).order_by("sort_order"),
            "project": ListOfProjectStatus.objects.filter(
                is_deleted=False,
            ).order_by("sort_order"),
            "task": ListOfTaskStatus.objects.filter(
                is_deleted=False,
            ).order_by("sort_order"),
        }

    @staticmethod
    def _get_tags():
        return Tag.objects.filter(
            is_deleted=False,
        ).order_by("name")

    @staticmethod
    def _get_types():
        return {
            "requirement": ListOfRequirementType.objects.filter(
                is_deleted=False,
            ).values("id", "type"),
            "requirement_item": ListOfRequirementItemType.objects.filter(
                is_deleted=False,
            ).values("id", "type"),
        }

    def get(self, request, *args, **kwargs):
        """Get method to retrieve initial data required by user"""
        user_results = User.objects.filter(
            username=request.user,
        ).annotate(
            profile_picture=F("userprofilepicture__document__key")
        )

        # Check to make sure we have one record only - error otherwise
        if len(user_results) != 1:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Defined user_result
        user_result = user_results.first()

        # Extra required data
        user_result.permissions = self._get_permissions(request.user)
        user_result.object_status = self._get_status()
        user_result.object_types = self._get_types()
        user_result.tags = self._get_tags()

        # Serialize data
        serializer = UserInitialDataSerializer(user_result)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
