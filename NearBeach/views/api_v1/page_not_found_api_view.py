from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    exclude=True,
)
class PageNotFoundView(APIView):
    @staticmethod
    def connect(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def delete(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def head(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def options(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def patch(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def post(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def put(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def trace(request, *args, **kwargs):
        return Response(
            data={"Error": "Page not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
