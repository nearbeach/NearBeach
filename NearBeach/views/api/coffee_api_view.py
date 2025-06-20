from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response


@extend_schema(
    exclude=True,
)
class CoffeeViewSet(viewsets.ViewSet):
    serializer_class = None

    @staticmethod
    def create(request, *args, **kwargs):
        return Response(
            data={"Teapot": "Why did you put coffee in me?"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def destroy(request, *args, **kwargs):
        return Response(
            data={"Teapot": "HEY!!! Don't break things"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def list(request, *args, **kwargs):
        return Response(
            data={"Teapot": "Hello, did you want to make some tea"},
            status=status.HTTP_418_IM_A_TEAPOT
        )

    @staticmethod
    def retrieve(request, *args, **kwargs):
        return Response(
            data = {"Teapot": "Sorry, I'm a teapot"},
            status = status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def update(request, pk=None, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, teapot can not be upgraded to coffee pot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )
