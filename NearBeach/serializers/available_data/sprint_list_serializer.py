from rest_framework import serializers
from NearBeach.models import Sprint


class SprintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            "sprint_id",
            "sprint_name",
            "sprint_start_date",
            "sprint_end_date",
        ]