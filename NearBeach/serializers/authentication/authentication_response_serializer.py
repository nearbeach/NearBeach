from rest_framework import serializers

from NearBeach.utils.enums.login_status_enum import LoginStatusEnum


class AuthenticationResponseSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=False,
    )
    status = serializers.CharField(
        default=LoginStatusEnum.TWO_FACTOR_REQUIRED,
    )
