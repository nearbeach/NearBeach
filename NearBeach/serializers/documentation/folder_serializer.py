from rest_framework import serializers
from NearBeach.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    """Class for folder serialization"""

    class Meta:
        model = Folder
        fields = [
            'id',
            'description',
            'parent_folder',
        ]
