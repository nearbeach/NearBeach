from rest_framework import serializers
from NearBeach.models import Tag


class TagsSerializer(serializers.ModelSerializer):
    """Class dealing with tags serializer"""
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'colour',
            'text_colour',
        ]
