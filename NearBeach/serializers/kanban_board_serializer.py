from rest_framework import serializers
from NearBeach.models import (
    Group,
    KANBAN_BOARD_STATUS_CHOICE,
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    KanbanLevel,
    OBJECT_CARD_PRIORITY,
    OBJECT_HIGHER_ORDER_STATUS,
)
from NearBeach.serializers.kanban_column_serializer import KanbanColumnSerializer
from NearBeach.serializers.kanban_level_serializer import KanbanLevelSerializer
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer


class KanbanBoardSerializer(serializers.Serializer):
    column_property = serializers.ChoiceField(
        required=False,
        choices=OBJECT_HIGHER_ORDER_STATUS,
    )
    column_title = serializers.CharField(
        max_length=255,
        required=False,
    )
    group_list = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=True,
        write_only=True,
    )
    kanban_board_id = serializers.IntegerField(
        read_only=True,
    )
    kanban_board_name = serializers.CharField(
        max_length=255,
        required=True,
    )
    kanban_board_status = serializers.ChoiceField(
        default="Open",
        choices=KANBAN_BOARD_STATUS_CHOICE,
        read_only=True,
    )
    kanban_column = KanbanColumnSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    kanban_level = KanbanLevelSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    kanban_card = KanbanCardSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    level_title = serializers.CharField(
        required=False,
        max_length=255,
    )
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new task
        if self.context["request"].method == "POST":
            fields.pop("kanban_board_status", None)
            fields["column_property"].required = True
            fields["column_title"].required = True
            fields["level_title"].required = True

        # Updating a new task
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)

        return fields
