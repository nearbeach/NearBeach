from rest_framework import serializers
from NearBeach.models import Group


class GroupListSerializer(serializers.Serializer):
    """Class containing serializer for adding/removing groups to objects"""
    group_list = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
    )
