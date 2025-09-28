from drf_spectacular.utils import extend_schema, OpenApiExample
from NearBeach.views.api.sprint_api_view import SprintViewSet
from NearBeach.models import SprintObjectAssignment, Sprint
from NearBeach.serializers.sprint_object_serializer import SprintObjectSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


@extend_schema(
    tags=["Sprint"]
)
class SprintLinkViewSet(SprintViewSet):
    # Setup the queryset and serialize class
    queryset = SprintObjectAssignment.objects.filter(is_deleted=False)
    serializer_class = SprintObjectSerializer
    http_method_names = ['get', 'post', 'delete']

    @staticmethod
    def _check_sprint(kwargs):
        # Check to make sure sprint exists
        get_object_or_404(
            queryset=Sprint.objects.filter(
                is_deleted=False,
            ),
            sprint_id=kwargs['sprint_id'],
        )

    @extend_schema(
        description="""
    # 📌 Description

    This endpoint links an object to the current sprint. The objects you can link are;
    - Requirement Items
    - Projects
    - Tasks


    # 🌏 Url

    - Destination: The parent object of the sprint:
        - Project
        - Requirement
    - Location ID: The unique ID of the parent object.


    # 🧾 Parameters

    - Object Type: The object we are currently trying to link. These will be;
        - Requirement Item
        - Project
        - Task
    - Object Id: A list of ID's for the objects (of type) we are currently trying to link
            """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Add task 2 to the sprint 3. Please note the url will be `/api/v0/project/2/object_sprint/3/`",
                value={
                    "object_id": 2,
                    "object_type": "task",
                },
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check to make sure sprint exists
        self._check_sprint(kwargs)

        for single_id in serializer.data["object_id"]:
            sprint_object_assignment = SprintObjectAssignment(
                **{F"{serializer.data['object_type']}_id": single_id},
                change_user=request.user,
                sprint_id_id=kwargs['sprint_id'],
            )
            sprint_object_assignment.save()

        # Get the new list of object results
        object_results = self._get_object_results(kwargs['sprint_id'])
        serializer = SprintObjectSerializer(object_results, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk, *args, **kwargs):
        self._check_sprint(kwargs)

        SprintObjectAssignment.objects.filter(
            pk=pk
        ).update(
            is_deleted=True,
            change_user=request.user,
        )

        # Get the new list of object results
        object_results = self._get_object_results(kwargs['sprint_id'])
        serializer = SprintObjectSerializer(object_results, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_204_NO_CONTENT,
        )

    def list(self, request, *args, **kwargs):
        self._check_sprint(kwargs)
        
        # Get the data
        object_results = self._get_object_results(kwargs['sprint_id'])
        serializer = SprintObjectSerializer(object_results, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""Method not used"""
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @extend_schema(
        description="""Method not used"""
    )
    def update(self, request, pk, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )