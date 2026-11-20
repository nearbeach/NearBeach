from rest_framework import serializers
from NearBeach.models import KanbanLevel


class KanbanLevelSerializer(serializers.ModelSerializer):
    """Class containing serializer base for all objects"""

    id = serializers.IntegerField(
        read_only=True,
    )
    name = serializers.CharField(
        max_length=255,
        required=True,
    )
    sort_number = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model = KanbanLevel

        fields = [
            "id",
            "name",
            "sort_number",
        ]
