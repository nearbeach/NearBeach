from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes

from NearBeach.serializers.authentication.forgotten_password_serializer import ForgottenPasswordSerializer
from NearBeach.services.AsyncEmailService import AsyncEmailService


class ForgottenPasswordView(APIView):
    """Class dealing with forgotten password"""
    permission_classes = [AllowAny]
    serializer_class = ForgottenPasswordSerializer

    @staticmethod
    def _handle_email(request, user):
        # Generate the user token and url
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Context
        context = {
            'url': request.scheme + "://" + request.get_host() + F"/login/reset-password/?uid={uid}&token={token}",
            'user': user,
        }

        # Send email
        AsyncEmailService(
            subject="NearBeach Password Reset",
            template="NearBeach/email/password_reset_email.html",
            recipient_list=[user.email],
            context=context,
        ).start()

    def post(self, request):
        serializer = ForgottenPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the user async
        users = User.objects.filter(
            email=serializer.validated_data['email'],
            is_active=True,
        )

        # Check to make sure we have the user
        for user in users:
            self._handle_email(request, user)

        return Response(status=status.HTTP_200_OK)
