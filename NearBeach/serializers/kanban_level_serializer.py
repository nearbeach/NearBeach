from rest_framework import serializers
from NearBeach.models import KanbanLevel


class KanbanLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanLevel
        fields = [
            "kanban_level_id",
            "kanban_level_name",
            "kanban_level_sort_number",
            "kanban_board"
        ]
