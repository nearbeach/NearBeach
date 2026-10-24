"""Swagger/OpenAPI documentation for PotentialObjectLinksViewSet."""
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from NearBeach.serializers.object_data.link_serializer import LinkSerializer

POTENTIAL_OBJECT_LINKS_SCHEMA = {
    "list": extend_schema(
        tags=["Search"],
        summary="List objects that can be linked",
        description=(
            "Projects, requirements, requirement items and tasks that belong to a group "
            "the user is in."
        ),
        parameters=[
            OpenApiParameter(
                name="q", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                required=False, description="Search string",
            ),
        ],
        responses={200: LinkSerializer(many=True)},
    ),
}
