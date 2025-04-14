from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from NearBeach.models import (
    Tag,
)
from NearBeach.serializers.available_data.tag_list_serializer import TagListSerializer


@extend_schema(
    tags=["Available Data"]
)
class TagListViewSet(viewsets.ViewSet):
    serializer_class = TagListSerializer

    def list(self, request, *args, **kwargs):
        tag_results = Tag.objects.filter(
            is_deleted=False,
        )

        serializer = TagListSerializer(
            tag_results,
            many=True,
        )

        return Response(serializer.data)
