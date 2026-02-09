from rest_framework import serializers
from NearBeach.models import (
    Group,
)
from NearBeach.serializers.parent_group_serializer import ParentGroupSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Class containing serializer for Groups"""
    id = serializers.ReadOnlyField(source='pk')
    name = serializers.CharField(
        required=True,
    )
    parent_group = ParentGroupSerializer(
        many=False,
        allow_null=True,
    )

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'parent_group',
        ]
