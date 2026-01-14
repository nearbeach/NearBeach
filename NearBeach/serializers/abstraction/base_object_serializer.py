from rest_framework import serializers

from NearBeach.models import Group


class BaseObjectSerializer(serializers.Serializer):
    """Class containing serializer base for all objects"""

    description = serializers.CharField(
        required=False,
    )

    group_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=False,
        write_only=True,
    )

    id = serializers.IntegerField(
        read_only=True,
    )

    title = serializers.CharField(
        max_length=255,
        required=True,
    )