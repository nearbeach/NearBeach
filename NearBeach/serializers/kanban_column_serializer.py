from rest_framework import serializers
from NearBeach.models import KanbanColumn


class KanbanColumnSerializer(serializers.ModelSerializer):
    kanban_column_sort_number = serializers.ReadOnlyField()
    kanban_column_property = serializers.CharField(
        required=True,
    )

    class Meta:
        model = KanbanColumn
        fields = [
            "kanban_column_id",
            "kanban_column_name",
            "kanban_column_property",
            "kanban_column_sort_number",
            # "kanban_board"
        ]
