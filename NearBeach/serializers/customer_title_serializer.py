from rest_framework import serializers
from NearBeach.models import ListOfTitle


class CustomerTitleSerializer(serializers.ModelSerializer):
    """Class containing serializer for Customer Title"""
    class Meta:
        model = ListOfTitle
        fields = [
            "id",
            "title",
        ]
