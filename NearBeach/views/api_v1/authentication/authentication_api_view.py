from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django_otp import user_has_device

from NearBeach.serializers.authentication.authentication_serializer import AuthenticationSerializer
from NearBeach.utils.admin import initalize_base_values
from NearBeach.utils.enums.login_status_enum import LoginStatusEnum


class AuthenticationView(APIView):
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if not serializer.is_valid():
            # Place the error into the message field
            serializer.message = serializer.errors

            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(username=serializer.username, password=serializer.password)

        # Check user is authenticated
        if user is None:
            serializer.status = LoginStatusEnum.INCORRECT_LOGIN

            return Response(
                serializer.data,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check first time login
        initalize_base_values(user)

        # User is logged in - check to make sure they don't have any 2FA
        if user_has_device(user, confirmed=True):
            serializer.status = LoginStatusEnum.TWO_FACTOR_REQUIRED

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        # Log in the user
        login(request, user)

        # Notify front end we have successfully logged in
        serializer.status = LoginStatusEnum.SUCCESS

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
