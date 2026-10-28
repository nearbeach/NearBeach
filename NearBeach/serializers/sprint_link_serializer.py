from rest_framework import serializers

from NearBeach.models.project import Project
from NearBeach.models.requirement.requirement import Requirement


class SprintLinkSerializer(serializers.Serializer):
    """Class for serializing sprint links"""
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.filter(
            is_deleted=False,
        ),
        required=False,
        write_only=True,
    )

    requirement = serializers.PrimaryKeyRelatedField(
        queryset=Requirement.objects.filter(
            is_deleted=False,
        ),
        required=False,
        write_only=True,
    )
