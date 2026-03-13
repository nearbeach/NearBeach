from django.contrib.auth.models import User
from rest_framework import serializers

from NearBeach.models import Group
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer


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

    user_list = UserSerializer(
        many=True,
        required=False,
        read_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()
        method = self.context.get('method', None)

        # GET
        if method == "GET":
            fields["group_list"] = GroupSerializer(
                many=True,
                read_only=True,
                required=False,
            )

        # PATCH
        if method == "PATCH":
            fields.pop("group_list", None)

        return fields
