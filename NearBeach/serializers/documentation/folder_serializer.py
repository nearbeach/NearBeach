from rest_framework import serializers
from NearBeach.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    """Class for folder serialization"""
    id = serializers.IntegerField(
        read_only=True
    )
    description = serializers.CharField(
        required=False,
    )
    parent_folder_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Folder
        fields = [
            'id',
            'description',
            'parent_folder_id',
        ]
