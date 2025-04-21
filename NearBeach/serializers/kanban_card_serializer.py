from rest_framework import serializers
from NearBeach.models import KanbanCard


class KanbanCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanCard
        exclude = [
            "is_archived",
            "date_modified",
            "change_user",
            "is_deleted",
        ]
