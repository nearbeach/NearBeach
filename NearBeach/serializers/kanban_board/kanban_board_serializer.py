from NearBeach.models import KanbanBoard
from NearBeach.serializers.kanban_board.kanban_card_serializer import KanbanCardSerializer
from NearBeach.utils.enums.kanban_board_enums import KanbanBoardStatusChoice
from rest_framework import serializers
from NearBeach.serializers.abstraction.meta_data_serializer_mixin import MetaDataSerializerMixin
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class KanbanBoardSerializer(MetaDataSerializerMixin, serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    kanban_card = KanbanCardSerializer(
        read_only=True,
        many=True,
    )
    status = EnumField(
        enum=KanbanBoardStatusChoice,
        required=True,
    )

    def create(self, validated_data):
        """Method for creating a kanban_board"""
        group_list = validated_data.pop("group_list", [])

        # Create the kanban_board
        kanban_board = KanbanBoard.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new kanban_board
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                kanban_board=kanban_board,
                change_user=validated_data["change_user"],
                creation_user=validated_data["creation_user"],
            )
            submit_object_assignment.save()

        return kanban_board

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)

        if method == "GET":
            fields["group_list"] = GroupSerializer(
                many=True,
                read_only=True,
                required=False,
            )

            fields["user_list"] = UserSerializer(
                many=True,
                read_only=True,
                required=False,
            )

        return fields

    class Meta:
        model = KanbanBoard
        fields = [
            "id",
            "title",
            "status",
            "kanban_card",
            "group_list",
            "user_list",
            "date_modified",
            "meta_data",
        ]


class KanbanBoardDetailSerializer(KanbanBoardSerializer):
    """The shape of a single kanban_board (GET): groups are readable here and the users are included.

    Exists so the API documentation can describe retrieve accurately; the endpoint itself passes
    `context={"method": "GET"}` to KanbanBoardSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "GET"}

        return super().get_fields()


class KanbanBoardPatchSerializer(KanbanBoardSerializer):
    """The PATCH shape of a kanban_board - request and response (no groups, organisation or users; status is an id).

    Exists so the API documentation can describe PATCH accurately; the endpoint itself passes
    `context={"method": "PATCH"}` to KanbanBoardSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "PATCH"}
        fields = super().get_fields()

        # Read-only, and only ever filled in by a GET of a single kanban_board
        fields.pop("user_list", None)

        return fields
