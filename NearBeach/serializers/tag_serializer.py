from rest_framework import serializers
from NearBeach.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = [
            "date_created",
            "date_modified",
            "change_user",
            "is_deleted",
        ]
