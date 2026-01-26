from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django_otp import user_has_device

from NearBeach.serializers.authentication.authentication_serializer import AuthenticationSerializer
from NearBeach.utils.admin import initalize_base_values
from NearBeach.utils.enums.login_status_enum import LoginStatusEnum


class AuthenticationView(APIView):
    permission_classes = [AllowAny]
    serializer: AuthenticationSerializer = None

    def _handle_two_factor(self, request, user):
        # Email the user their code
        # device, created = EmailDevice.objects.get_or_create(
        #     user=user,
        #     name=user.username,
        #     confirmed=True
        # )

        # TEMP CODE
        device_totp, created_totp = TOTPDevice.objects.get_or_create(
            user=user,
            name=user.username,
            confirmed=True
        )
        # END TEMP CODE

        # Get the otp token from the serializer
        otp_token = self.serializer.validated_data['otp_token']

        # If user has not supplied the OTP - send them a request for it
        if otp_token is None or otp_token == "":
            # Generate code
            # device.generate_challenge()
            # device_totp.generate_challenge()

            return Response(
                data={'status': LoginStatusEnum.TWO_FACTOR_REQUIRED},
                status=status.HTTP_200_OK,
            )

        # Verify 2fa
        if not device_totp.verify_token(otp_token):
            return Response(
                data={'status': LoginStatusEnum.FAILURE},
                status=status.HTTP_403_FORBIDDEN,
            )

        # User passed all tests
        return self._login(request, user)

    def _login(self, request, user):
        login(request, user)

        return Response(
            data={'status': LoginStatusEnum.SUCCESS},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
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

        # User is logged in - check to make sure they don't have any 2FA
        if user_has_device(user, confirmed=True):
            return self._handle_two_factor(request, user)

        # Log user in
        return self._login(request, user)
