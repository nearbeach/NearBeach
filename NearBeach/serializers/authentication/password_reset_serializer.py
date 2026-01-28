from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
