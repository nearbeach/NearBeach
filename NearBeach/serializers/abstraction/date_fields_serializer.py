from rest_framework import serializers


class DateFieldsSerializer(serializers.Serializer):
    """Class containing serializer fields for dates"""
    end_date = serializers.DateTimeField(
        required=False,
    )

    start_date = serializers.DateTimeField(
        required=False,
    )