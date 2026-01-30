from rest_framework import serializers


class ForgottenPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
