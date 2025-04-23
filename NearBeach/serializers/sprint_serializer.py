from rest_framework import serializers
from NearBeach.models import (
    Project,
    Requirement,
    Sprint,
)
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.serializers.requirement_serializer import RequirementSerializer


class SprintSerializer(serializers.ModelSerializer):
    destination = serializers.ChoiceField(
        choices=(
            "requirement",
            "project",
        ),
        required=True,
    )
    location_id = serializers.IntegerField(
        required=True,
    )
    sprint_id = serializers.ReadOnlyField()
    sprint_name = serializers.CharField(
        required=True,
    )
    sprint_start_date = serializers.DateTimeField(
        required=True,
    )
    sprint_end_date = serializers.DateTimeField(
        required=True,
    )
    requirement = RequirementSerializer(
        many=False,
        allow_null=True,
        read_only=True,
    )
    project = ProjectSerializer(
        many=False,
        allow_null=True,
        read_only=True,
    )
    sprint_status = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_modified = serializers.ReadOnlyField()

    class Meta:
        model = Sprint
        exclude = [
            "change_user",
            "is_deleted",
        ]

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating a new task
        if self.context['request'].method == "DELETE":
            fields.pop("sprint_name", None)
            fields.pop("sprint_start_date", None)
            fields.pop("sprint_end_date", None)

        return fields
