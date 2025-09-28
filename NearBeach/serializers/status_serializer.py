from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    value = serializers.IntegerField(
        required=True,
    )
    label = serializers.CharField(
        required=True,
        max_length=100,
    )
    higher_order_status = serializers.CharField(
        required=True,
        max_length=10,
    )

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
