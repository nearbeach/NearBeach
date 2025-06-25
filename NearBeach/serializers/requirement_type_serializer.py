from rest_framework import serializers
from NearBeach.models import ListOfRequirementType


class RequirementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfRequirementType
        fields = [
            "requirement_type_id",
            "requirement_type",
        ]
