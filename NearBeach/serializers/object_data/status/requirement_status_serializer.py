from rest_framework import serializers
from NearBeach.models import ListOfRequirementStatus
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class RequirementStatusSerializer(serializers.ModelSerializer):
    """Class containing serializer for requirement status"""

    higher_order_status = EnumField(enum=ObjectHigherOrderStatus)

    class Meta:
        model = ListOfRequirementStatus
        fields = [
            "id",
            "status",
            "higher_order_status",
        ]
