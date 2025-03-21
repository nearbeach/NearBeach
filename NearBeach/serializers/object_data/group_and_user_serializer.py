from rest_framework import serializers
from NearBeach.models import Group, User
from NearBeach.serializers.destination_serializer import DestinationSerializer


class GroupAndUserSerializer(DestinationSerializer):
    # Queryset Data
    group_results = Group.objects.filter(
        is_deleted=False,
    )
    user_results = User.objects.filter(
        is_active=True,
    )

    # Serialise Data
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=group_results,
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
        queryset=group_results,
    )
    user_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=User.objects.filter(
            is_active=True,
        )
    )
