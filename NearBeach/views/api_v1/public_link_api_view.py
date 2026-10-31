from rest_framework import viewsets
from rest_framework.response import Response
from NearBeach.services.PublicLinkService import PublicLinkService


class PublicLinkViewSet(viewsets.ViewSet):
    """Class for the public link view set"""
    http_method_names = ['get']
    lookup_value_regex = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

    @staticmethod
    def retrieve(request, pk, *args, **kwargs) -> Response:
        """Retrieve a single public link"""
        public_link_service = PublicLinkService(destination="public_link", location_id=pk)
        data, http_status = public_link_service.retrieve(request)

        return Response(
            data=data,
            status=http_status,
        )
