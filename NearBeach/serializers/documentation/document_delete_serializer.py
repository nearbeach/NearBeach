from rest_framework import serializers


class DocumentDeleteSerializer(serializers.Serializer):
    """Class for document serialization"""
    type = serializers.ChoiceField(
        write_only=True,
        choices=[
            'document',
            'folder',
            'link'
        ]
    )