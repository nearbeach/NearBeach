from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from NearBeach.serializers.authentication.password_reset_serializer import PasswordResetSerializer


class ForgottenPasswordView(APIView):
    """Class dealing with forgotten password"""
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        
