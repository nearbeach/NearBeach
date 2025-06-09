from rest_framework import serializers
from NearBeach.models import (
    Group,
    KANBAN_BOARD_STATUS_CHOICE,
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    KanbanLevel,
    OBJECT_HIGHER_ORDER_STATUS, ObjectAssignment,
)
from NearBeach.serializers.kanban_column_serializer import KanbanColumnSerializer
from NearBeach.serializers.kanban_level_serializer import KanbanLevelSerializer
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer


class KanbanBoardSerializer(serializers.Serializer):
    group_list = serializers.PrimaryKeyRelatedField(
        many=True,
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
    kanban_column = serializers.ListSerializer(
        child=KanbanColumnSerializer(),
    )
    kanban_level = serializers.ListSerializer(
        child=KanbanLevelSerializer(),
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

    def create(self, validated_data):
        # Pop out the fields we don't need
        group_list = validated_data.pop("group_list", [])
        kanban_column_list = validated_data.pop("kanban_column", [])
        kanban_level_list = validated_data.pop("kanban_level", [])

        # Extract data we need

        # Create the kanban board
        kanban_board = KanbanBoard.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new project
            submit_object_assignment = ObjectAssignment(
                group_id=single_group,
                kanban_board=kanban_board,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        # Create the required columns
        for index, kanban_column in enumerate(kanban_column_list, start=0):
            submit_kanban_column = KanbanColumn(
                kanban_column_name=kanban_column["kanban_column_name"],
                kanban_column_property=kanban_column["kanban_column_property"],
                kanban_column_sort_number=index,
                kanban_board=kanban_board,
                change_user=validated_data["change_user"],
            )
            submit_kanban_column.save()

        # Create the required levels
        for index, kanban_level in enumerate(kanban_level_list, start=0):
            submit_kanban_level = KanbanLevel(
                kanban_level_name=kanban_level["kanban_level_name"],
                kanban_level_sort_number=index,
                kanban_board=kanban_board,
                change_user=validated_data["change_user"],
            )
            submit_kanban_level.save()

        return kanban_board

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new task
        if self.context["request"].method == "POST":
            fields.pop("kanban_board_status", None)
            # fields["column_property"].required = True
            # fields["column_title"].required = True
            # fields["level_title"].required = True
            # fields["column_property"].many = True
            # fields["column_title"].many = True
            # fields["level_title"].many = True


        # Updating a new task
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)

        return fields
