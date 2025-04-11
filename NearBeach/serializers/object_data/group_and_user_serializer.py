from rest_framework import serializers
from NearBeach.models import Group, User


class GroupAndUserSerializer(serializers.Serializer):
    # Serialise Data
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
    )
    user = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=User.objects.filter(
            is_active=True,
        ),
    )
    group_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
    )
    user_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=User.objects.filter(
            is_active=True,
        )
    )
