from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F

from NearBeach.models import (
    UserGroup,
)
from NearBeach.serializers.user.permissions_serializer import PermissionSerializer


@extend_schema(
    exclude=True,
)
class PermissionView(APIView):
    """Class dealing with user permissions api"""
    serializer_class = None

    @staticmethod
    def get(request, *args, **kwargs):
        """Get method to retrieve a list of user permissions associated with the user"""
        results = UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
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

        serializer = PermissionSerializer(results, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
