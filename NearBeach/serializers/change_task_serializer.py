from rest_framework import serializers
from NearBeach.models import ChangeTask


class ChangeTaskSerializer(serializers.ModelSerializer):
    change_task_seconds = serializers.ReadOnlyField()
    change_task_status_name = serializers.CharField(
        source="get_change_task_status_display",
        read_only=True,
    )

    class Meta:
        model = ChangeTask
        exclude = [
            "creation_user",
            "change_user",
            "date_modified",
            "is_deleted",
        ]
