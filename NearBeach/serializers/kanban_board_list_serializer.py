from rest_framework import serializers
from NearBeach.models import (
    KanbanBoard,
)


class KanbanBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanBoard
        fields = [
            'kanban_board_id',
            'kanban_board_name',
            'kanban_board_status',
        ]