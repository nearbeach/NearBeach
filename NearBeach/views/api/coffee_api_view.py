from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.models import Project
from NearBeach.serializers.project_serializer import ProjectSerializer


class CoffeeViewSet(viewsets.ViewSet):
    @staticmethod
    def create(self, request, *args, **kwargs):
        return Response(
            data={"Teapot": "Why did you put coffee in me?"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    def list(self, request, *args, **kwargs):
        return Response(
            data={"Teapot": "Hello, did you want to make some tea"},
            status=status.HTTP_418_IM_A_TEAPOT
        )

    @staticmethod
    def retrieve(self, request, *args, **kwargs):
        return Response(
            data = {"Teapot": "Sorry, I'm a teapot"},
            status = status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def update(self, request, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, teapot can not be upgraded to coffee pot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def destroy(self, request, *args, **kwargs):
        return Response(
            data={"Teapot": "HEY!!! Don't break things"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )


