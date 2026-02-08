from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from NearBeach.serializers.authentication.password_reset_serializer import PasswordResetSerializer
from NearBeach.utils.throttle.AuthMinuteThrottle import AuthMinuteThrottle
from NearBeach.utils.throttle.AuthHourThrottle import AuthHourThrottle


class PasswordResetView(APIView):
    """Class dealing with forgotten password"""
    authentication_classes = []  # important for login
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer
    throttle_classes = [AuthMinuteThrottle, AuthHourThrottle]

    @staticmethod
    def _get_user(uid):
        """Method for retrieving a user by uid"""
        udi_bytes = urlsafe_base64_decode(uid)
        user_id = force_str(udi_bytes)

        return User.objects.filter(
            pk=user_id,
            is_active=True,
        ).first()

    def post(self, request, *args, **kwargs):
        """Method handling post requests for password reset"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user
        user = self._get_user(serializer.validated_data['uid'])
        if user is None:
            # Silently fail - ensure the attacker that the password has updated
            return Response(
                status=status.HTTP_200_OK,
            )

        # Verify token
        is_token_valid = PasswordResetTokenGenerator().check_token(user, serializer.validated_data['token'])
        if not is_token_valid:
            # Notify the user that the token has expired
            return Response(
                data={"message": "Token has expired and no longer valid"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Reset the user's password
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Send user 200 response
        return Response(status=status.HTTP_200_OK)
