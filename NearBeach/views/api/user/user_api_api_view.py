from django.contrib.auth.decorators import user_passes_test
from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from knox.auth import TokenAuthentication
from NearBeach.utils.api.permissions import IsSuperUser
from NearBeach.serializers.user.user_api_serializer import UserApiSerializer
from NearBeach.models import ExtendsAuthToken
from django.db.models import F


@extend_schema(
    tags=['User|User API'],
    methods=["GET", "POST", "DELETE"],
)
class UserApiViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = ExtendsAuthToken.objects.all()
    serializer_class = UserApiSerializer
    permission_classes = [IsSuperUser]

    @extend_schema(
        description="""
# 📌 Description

Creates a single API Key against the user

# 🧾 Parameters 
- Description: Description of the API Key
- Expires In: Integer for how many days until the key expires. Leave blank for keys that you do not want to expire
        """
    )
    def create(self, request, *args, **kwargs):
        serializer = UserApiSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save
        created_api_key = serializer.save(
            user=kwargs['username'],
            change_user=request.user,
        )

        # Re-serialize
        serializer = UserApiSerializer(
            created_api_key,
            many=False,
            context={"request": request},
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Deletes a single API Key from a user
        """
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        extend_auth_token = ExtendsAuthToken.objects.get(pk=pk)
        extend_auth_token.delete()
        return Response(
            data={"API Key Deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all API Keys for a user
        """
    )
    def list(self, request, *args, **kwargs):
        extends_auth_token = ExtendsAuthToken.objects.filter(
            user_id=kwargs['username'],
        ).annotate(
            api_key=F("token_key"),
        )

        serializer = UserApiSerializer(
            extends_auth_token,
            many=True,
            context={"request": request},
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
