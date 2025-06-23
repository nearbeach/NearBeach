from rest_framework import serializers
from NearBeach.models import (
    Group,
    Task, ListOfTaskStatus, Organisation, ObjectAssignment,
)
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.task_status_serializer import TaskStatusSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority


class TaskSerializer(serializers.ModelSerializer):
    group_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=True,
        write_only=True,
    )
    organisation = OrganisationSerializer(
        many=False,
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
    task_priority = EnumField(enum=ObjectPriority)
    task_start_date = serializers.DateTimeField(
        required=True,
    )
    task_status = TaskStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
    )
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )
    
    def create(self, validated_data):
        # Pop out the filed we don't need
        group_list = validated_data.pop("group_list", [])
        
        # Extract the data we need
        validated_data["task_status"] = ListOfTaskStatus.objects.filter(
            is_deleted=False,
        ).order_by(
            "task_status_sort_order",
        ).first()
        
        # Create the task
        task = Task.objects.create(**validated_data)
        
        # Create the group list
        for single_group in group_list:
            # Save the group against the new project
            submit_object_assignment = ObjectAssignment(
                group_id=single_group,
                task=task,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        return task

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new task
        if self.context["request"].method == "POST":
            fields.pop("task_status", None)
            fields.pop("task_priority", None)
            fields["organisation"] = serializers.PrimaryKeyRelatedField(
                queryset=Organisation.objects.filter(
                    is_deleted=False,
                )
            )

        # Updating a new task
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)
            fields.pop("organisation", None)
            fields["task_status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfTaskStatus.objects.filter(
                    is_deleted=False,
                ),
            )

        return fields

    def update(self, instance, validated_data):
        # Task Status
        task_status_id = validated_data.pop("task_status", 0)
        instance.task_status_id = task_status_id

        # Prioirty
        task_priority = validated_data.pop("task_priority")
        instance.task_priority = task_priority["value"]

        # Update instance
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Task
        fields = [
            "task_id",
            "task_short_description",
            "task_long_description",
            "organisation",
            "task_status",
            "task_higher_order_status",
            "task_priority",
            "task_story_point",
            "task_start_date",
            "task_end_date",
            "date_created",
            "date_modified",
            "group_list",
            "uuid",
        ]