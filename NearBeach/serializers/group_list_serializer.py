from rest_framework import serializers
from NearBeach.models.user import Group


class GroupListSerializer(serializers.Serializer):
    """Class containing serializer for adding/removing groups to objects"""
    group_list = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        allow_empty=False,  # a form post with no group_list at all arrives as an empty list
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
    )
