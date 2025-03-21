from rest_framework import serializers
from NearBeach.models import Tag


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'tag_id',
            'tag_name',
            'tag_colour',
            'tag_text_colour',
        ]