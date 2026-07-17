from rest_framework import serializers
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer


class GroupAndUserSerializer(serializers.Serializer):
    """Class containing serializer for Groups and Users"""
    group_list = GroupSerializer(
        read_only=True,
        many=True,
        required=False,
    )

    potential_user_list = UserSerializer(
        read_only=True,
        many=True,
        required=False,
    )

    user_list = UserSerializer(
        read_only=True,
        many=True,
        required=False,
    )
