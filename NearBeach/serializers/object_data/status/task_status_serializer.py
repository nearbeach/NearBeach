from rest_framework import serializers
from NearBeach.models import ListOfTaskStatus
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    """Class containing serializer for task status"""

    higher_order_status = EnumField(enum=ObjectHigherOrderStatus)

    class Meta:
        model = ListOfTaskStatus
        fields = [
            "id",
            "status",
            "higher_order_status",
        ]
