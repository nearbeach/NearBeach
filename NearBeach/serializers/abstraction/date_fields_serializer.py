from rest_framework import serializers


class DateFieldsSerializer(serializers.Serializer):
    """Class containing serializer fields for dates"""
    end_date = serializers.DateField(
        required=False,
    )

    start_date = serializers.DateField(
        required=False,
    )