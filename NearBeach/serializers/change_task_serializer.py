from django.contrib.auth.models import User
from rest_framework import serializers
from NearBeach.models import ChangeTask


class ChangeTaskSerializer(serializers.ModelSerializer):
    change_task_seconds = serializers.ReadOnlyField()
    change_task_status_id = serializers.ReadOnlyField(
        source="change_task_status",
    )
    change_task_status_name = serializers.ReadOnlyField(
        source="get_change_task_status_display",
    )
    change_task_required_by = serializers.CharField(
        required=False,
    )
    is_downtime = serializers.CharField(
        required=False,
    )
    request_for_change = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    change_task_assigned_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    change_task_qa_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = ChangeTask
        exclude = [
            "change_task_status",
            "creation_user",
            "change_user",
            "date_modified",
            "date_created",
            "is_deleted",
        ]
