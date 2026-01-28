from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_static.models import StaticDevice
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django_otp import user_has_device, match_token

from NearBeach.serializers.authentication.authentication_serializer import AuthenticationSerializer
from NearBeach.utils.admin import initalize_base_values
from NearBeach.utils.enums.login_status_enum import LoginStatusEnum


class AuthenticationView(APIView):
    permission_classes = [AllowAny]
    serializer: AuthenticationSerializer = None

    def _check_user_two_factor_devices(self, user) -> list[str]:
        """Function to get a list of user's two-factor devices."""
        devices = []

        # Get list of all potential devices
        totp_device = TOTPDevice.objects.filter(user=user, confirmed=True)
        email_device = EmailDevice.objects.filter(
            user=user,
            confirmed=True
        )

        # Add the device to the array if it exists
        if totp_device.exists():
            devices.append("totp")

        if email_device.exists():
            devices.append("email")
            self._generate_email_token(user)

        return devices

    @staticmethod
    def _generate_email_token(user):
        """Function to generate a token for an user's two-factor devices."""
        email_device, created = EmailDevice.objects.get_or_create(
            user=user,
            confirmed=True
        )

        email_device.generate_challenge()

    def _handle_two_factor(self, request, user):
        """Handle the Two Factor verification and login request."""
        otp_token = self.serializer.validated_data['otp_token']

        device = match_token(user, otp_token)
        if device is None:
            return Response(
                data={'status': LoginStatusEnum.FAILURE},
                status=status.HTTP_403_FORBIDDEN,
            )

        # User passed all tests
        return self._login(request, user)

    @staticmethod
    def _login(request, user):
        """Function to login user and return success status"""
        login(request, user)

        return Response(
            data={'status': LoginStatusEnum.SUCCESS},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """Function to authenticate a user."""
        self.serializer = AuthenticationSerializer(data=request.data)
        if not self.serializer.is_valid():
            # Place the error into the message field
            self.serializer.message = self.serializer.errors

            return Response(
                self.serializer.data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(
            username=self.serializer.validated_data['username'],
            password=self.serializer.validated_data['password']
        )

        # Check user is authenticated
        if user is None:
            self.serializer.status = LoginStatusEnum.INCORRECT_LOGIN

            return Response(
                self.serializer.data,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check first time login
        initalize_base_values(user)

        # Check to see if user has a device
        devices = self._check_user_two_factor_devices(user)

        # User has not setup 2FA - log user in
        if len(devices) == 0:
            return self._login(request, user)
        # User has setup 2FA but has not supplied the otp_token
        elif self.serializer.validated_data['otp_token'] == "":
            # User has setup 2FA but has not supplied credentials
            return Response(
                data={'status': LoginStatusEnum.TWO_FACTOR_REQUIRED},
                status=status.HTTP_200_OK,
            )

        # Handle the two factor
        return self._handle_two_factor(request, user)

