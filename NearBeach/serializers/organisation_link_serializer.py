from rest_framework import serializers
from NearBeach.models import (
    Organisation,
)


class OrganisationLinkSerializer(serializers.ModelSerializer):
    """Class containing serializer for Organisation links"""
    id = serializers.IntegerField()

    class Meta:
        model = Organisation
        fields = [
            "id",
        ]
