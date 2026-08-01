from NearBeach.models import Sprint
from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.serializers.requirement_serializer import RequirementSerializer
from rest_framework import serializers

from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer


class SprintSerializer(serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer for Sprints"""
    project = ProjectSerializer(
        many=False,
        read_only=True,
        allow_null=True,
    )

    requirement = RequirementSerializer(
        many=False,
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Sprint
        fields = [
            "id",
            "title",
            "requirement",
            "project",
            "total_story_points",
            "completed_story_points",
            "status",
            "start_date",
            "end_date",
        ]