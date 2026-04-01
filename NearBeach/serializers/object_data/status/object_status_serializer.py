from rest_framework import serializers

from NearBeach.serializers.object_data.status.project_status_serializer import ProjectStatusSerializer
from NearBeach.serializers.object_data.status.requirement_item_status_serializer import RequirementItemStatusSerializer
from NearBeach.serializers.object_data.status.requirement_status_serializer import RequirementStatusSerializer
from NearBeach.serializers.object_data.status.task_status_serializer import TaskStatusSerializer


class ObjectStatusSerializer(serializers.Serializer):
    """Class contains object status serializer"""
    requirement = RequirementStatusSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )

    requirement_item = RequirementItemStatusSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )

    project = ProjectStatusSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )

    task = TaskStatusSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )

    class Meta:
        fields = [
            'requirement',
            'requirement_item',
            'project',
            'task',
        ]
