from rest_framework import serializers
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer


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