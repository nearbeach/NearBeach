from rest_framework import serializers
from NearBeach.models import ListOfRequirementType


class RequirementTypesSerializer(serializers.ModelSerializer):
    """Class containing serializer for the Requirement Types"""
    class Meta:
        model = ListOfRequirementType
        fields = [
            "id",
            "type",
        ]
