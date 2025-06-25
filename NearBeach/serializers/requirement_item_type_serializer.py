from rest_framework import serializers
from NearBeach.models import ListOfRequirementItemType


class RequirementItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfRequirementItemType
        fields = [
            "requirement_item_type_id",
            "requirement_item_type",
        ]
