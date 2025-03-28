from rest_framework import viewsets
from rest_framework.response import Response

from NearBeach.models import (
    Tag,
)
from NearBeach.serializers.available_data.tag_list_serializer import TagListSerializer


class TagListViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        tag_results = Tag.objects.filter(
            is_deleted=False,
        )

        serializer = TagListSerializer(
            tag_results,
            many=True,
        )

        return Response(serializer.data)
