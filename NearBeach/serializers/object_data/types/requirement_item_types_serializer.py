from rest_framework import serializers
from NearBeach.models.requirement.requirement_item import ListOfRequirementItemType


class RequirementItemTypesSerializer(serializers.ModelSerializer):
    """Class containing serializer for the Requirement Item Types"""
    class Meta:
        model = ListOfRequirementItemType
        fields = [
            "id",
            "type",
        ]