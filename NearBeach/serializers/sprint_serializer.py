from rest_framework import serializers
from NearBeach.models import (
    Sprint, Project, Requirement,
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

    object_dict = {
        "project": Project.objects,
        "requirement": Requirement.objects,
    }

    def create(self, validated_data):
        # Connect the object
        destination = validated_data.pop("destination")
        location_id = validated_data.pop("location_id")

        validated_data[destination] = self.object_dict[destination].get(
            **{F"{destination}_id": location_id},
        )

        sprint = Sprint.objects.create(**validated_data)

        return sprint

    class Meta:
        model = Sprint
        fields = [
            "sprint_id",
            "sprint_name",
            "sprint_status",
            "destination",
            "location_id",
            "sprint_start_date",
            "sprint_end_date",
            "total_story_points",
            "completed_story_points",
            "requirement",
            "project",
            "date_created",
            "date_modified",
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
