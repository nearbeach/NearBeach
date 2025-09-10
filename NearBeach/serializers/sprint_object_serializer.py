from rest_framework import serializers


class SprintObjectSerializer(serializers.Serializer):
    description = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    end_date = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    higher_order_status = serializers.CharField(
        read_only=True,
        max_length=10,
        allow_null=True,
    )
    object_id = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    object_type = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    parent_object_type = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    parent_object_id = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    start_date = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    status_id = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    title = serializers.CharField(
        max_length=255,
        read_only=True,
        allow_null=True,
    )
