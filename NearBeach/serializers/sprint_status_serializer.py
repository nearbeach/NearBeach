from rest_framework import serializers
from NearBeach.serializers.status_serializer import StatusSerializer


class SprintStatusSerializer(serializers.Serializer):
    requirement_item = StatusSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    project = StatusSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    task = StatusSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
