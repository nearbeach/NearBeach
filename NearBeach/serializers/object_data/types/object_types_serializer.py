from rest_framework import serializers

from NearBeach.serializers.object_data.types.requirement_item_types_serializer import RequirementItemTypesSerializer
from NearBeach.serializers.object_data.types.requirement_types_serializer import RequirementTypesSerializer


class ObjectTypesSerializer(serializers.Serializer):
    """Class containing serializer for the object types"""
    requirement = RequirementTypesSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )
    requirement_item = RequirementItemTypesSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )
