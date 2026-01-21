from rest_framework import serializers
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.login_status_enum import LoginStatusEnum

class AuthenticationSerializer(serializers.Serializer):
    message = serializers.CharField(
        read_only=True,
        required=False,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    status = EnumField(
        default=LoginStatusEnum.FAILURE,
        enum=LoginStatusEnum,
        read_only=True,
    )
    username = serializers.CharField(
        required=True,
        write_only=True,
    )
