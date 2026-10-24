# TODO - Requirement is not defined in NearBeach.models.project, so importing this module raises ImportError.
#  Nothing imports it yet; it should come from NearBeach.models.requirement.requirement
from NearBeach.models.project import Project, Requirement
from rest_framework import serializers


class SprintLinkSerializer(serializers.Serializer):
    """Class for serializing sprint links"""
    project = serializers.ChoiceField(
        choices=Project.objects.filter(
            is_deleted=False,
        ),
        required=False,
        write_only=True,
    )

    requirement = serializers.ChoiceField(
        choices=Requirement.objects.filter(
            is_deleted=False,
        ),
        required=False,
        write_only=True,
    )
