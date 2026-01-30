from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    token = serializers.CharField(
        required=True,
        write_only=True,
    )
    uid = serializers.CharField(
        required=True,
        write_only=True,
    )
