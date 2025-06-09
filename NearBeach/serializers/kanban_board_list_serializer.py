from rest_framework import serializers
from NearBeach.models import (
    Group,
    KANBAN_BOARD_STATUS_CHOICE,
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    KanbanLevel,
    OBJECT_HIGHER_ORDER_STATUS,
)
from NearBeach.serializers.kanban_column_serializer import KanbanColumnSerializer
from NearBeach.serializers.kanban_level_serializer import KanbanLevelSerializer
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer


class KanbanBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanBoard
        fields = [
            'kanban_board_id',
            'kanban_board_name',
            'kanban_board_status',
        ]