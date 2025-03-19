from rest_framework import serializers
from NearBeach.models import Customer


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "customer_first_name",
            "customer_last_name",
            "customer_email",
        ]