from rest_framework import serializers
from NearBeach.models import (
    Group,
    ListOfTaskStatus,
    OBJECT_CARD_PRIORITY,
    Organisation,
)


class TaskSerializer(serializers.Serializer):
    group_list = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=True,
        write_only=True,
    )
    organisation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Organisation.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    organisation_name = serializers.ReadOnlyField(
        source='organisation.organisation_name',
    )
    task_end_date = serializers.DateTimeField(
        required=True,
    )
    task_higher_order_status = serializers.ReadOnlyField(
        source='task_status.task_higher_order_status',
    )
    task_id = serializers.IntegerField(
        read_only=True,
    )
    task_long_description = serializers.CharField(
        required=True,
    )
    task_short_description = serializers.CharField(
        max_length=255,
        required=True,
    )
    task_priority = serializers.ChoiceField(
        choices=OBJECT_CARD_PRIORITY,
    )
    task_priority_name = serializers.ReadOnlyField(
        source='get_task_priority_display',
    )
    task_start_date = serializers.DateTimeField(
        required=True,
    )
    task_status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ListOfTaskStatus.objects.filter(
            is_deleted=False,
        ),
    )
    task_status_name = serializers.ReadOnlyField(
        source='task_status.task_status',
    )
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new task
        if self.context["request"].method == "POST":
            fields.pop("task_status", None)
            fields.pop("task_priority", None)

        # Updating a new task
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)
            fields.pop("organisation_id", None)

        return fields
