from rest_framework import serializers
from NearBeach.models import ListOfTaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfTaskStatus
        fields = [
            "task_status_id",
            "task_status",
        ]