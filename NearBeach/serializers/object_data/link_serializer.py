from rest_framework import serializers
from NearBeach.models import (
    ChangeTask,
    Project,
    Requirement,
    RequirementItem,
    Task,
)


class LinkSerializer(serializers.Serializer):
    change_task = serializers.PrimaryKeyRelatedField(
        queryset=ChangeTask.objects.all(),
        required=False,
    )
    link_relationship = serializers.CharField(
        read_only=True,
    )
    object_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    object_id = serializers.IntegerField(
        read_only=True,
    )
    object_title = serializers.CharField(
        read_only=True,
    )
    object_status = serializers.CharField(
        read_only=True,
    )
    object_type = serializers.CharField(
        read_only=True,
    )
    parent_link = serializers.CharField(
        read_only=True,
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        required=False,
    )
    requirement = serializers.PrimaryKeyRelatedField(
        queryset=Requirement.objects.all(),
        required=False,
    )
    requirement_item = serializers.PrimaryKeyRelatedField(
        queryset=RequirementItem.objects.all(),
        required=False,
    )
    reverse_relation = serializers.BooleanField(
        read_only=True,
    )
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
    )
    object_relation = serializers.CharField(
        required=False,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # If creating a new link, we'll need the object relation
        if self.context["request"].method == "POST":
            fields["object_relation"].required = True

        return fields
