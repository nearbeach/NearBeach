from rest_framework import serializers
from NearBeach.models import ListOfProjectStatus
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ProjectStatusSerializer(serializers.ModelSerializer):
    """Class containing serializer for project status"""

    higher_order_status = EnumField(enum=ObjectHigherOrderStatus)
    

    class Meta:
        model = ListOfProjectStatus
        fields = [
            "id",
            "status",
            "higher_order_status",
        ]
