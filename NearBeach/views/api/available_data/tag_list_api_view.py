from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.models import (
    Tag,
)
from NearBeach.serializers.available_data.tag_list_serializer import TagListSerializer


@extend_schema(
    tags=["Available Data|Tag List"]
)
class TagListViewSet(viewsets.ViewSet):
    serializer_class = TagListSerializer

    @extend_schema(
        description="""
# 📌 Description

Present a list of all tags to the user

        """,
        responses={200: TagListSerializer},
    )
    def list(self, request, *args, **kwargs):
        tag_results = Tag.objects.filter(
            is_deleted=False,
        )

        serializer = TagListSerializer(
            tag_results,
            many=True,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
