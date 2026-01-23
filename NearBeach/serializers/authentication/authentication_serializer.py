from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    otp_token = serializers.CharField(
        allow_blank=True,
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    username = serializers.CharField(
        required=True,
        write_only=True,
    )
