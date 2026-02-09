from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.models import Project
from NearBeach.serializers.project_serializer import ProjectSerializer


@extend_schema(
    tags=["Projects"],
    methods=["GET", "POST", "PUT", "DELETE"],
)
class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    # TODO - PERMISSIONS
    def create(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Why did you put coffee in me?"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def destroy(_, *args, **kwargs):
        return Response(
            data={"Teapot": "HEY!!! Don't break things"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def list(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Hello, did you want to make some tea"},
            status=status.HTTP_418_IM_A_TEAPOT
        )

    @staticmethod
    def partial_update(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, teapot can not be upgraded to coffee pot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )

    @staticmethod
    def retrieve(_, *args, **kwargs):
        return Response(
            data={"Teapot": "Sorry, I'm a teapot"},
            status=status.HTTP_418_IM_A_TEAPOT,
        )
