from rest_framework import serializers
from NearBeach.models import ListOfRequirementItemStatus


class RequirementItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfRequirementItemStatus
        fields = [
            "requirement_item_status_id",
            "requirement_item_status",
            "requirement_item_higher_order_status",
        ]
