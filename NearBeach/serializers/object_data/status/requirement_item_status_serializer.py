from rest_framework import serializers
from NearBeach.models import ListOfRequirementItemStatus
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class RequirementItemStatusSerializer(serializers.ModelSerializer):
    """Class containing serializer for requirement item status"""

    higher_order_status = EnumField(enum=ObjectHigherOrderStatus)

    class Meta:
        model = ListOfRequirementItemStatus
        fields = [
            "id",
            "status",
            "higher_order_status",
        ]
