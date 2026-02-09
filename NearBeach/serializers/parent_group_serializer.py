from rest_framework import serializers
from NearBeach.models import (
    Group,
)


class ParentGroupSerializer(serializers.ModelSerializer):
    """Class containing serializer for Parent Groups"""
    # Name
    # Parent Group
    id = serializers.ReadOnlyField(source='pk')
    name = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
        ]
