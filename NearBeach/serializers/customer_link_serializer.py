from rest_framework import serializers
from NearBeach.models import (
    Customer,
)


class CustomerLinkSerializer(serializers.ModelSerializer):
    """Class containing serializer for Customer links"""
    id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = [
            "id",
        ]
