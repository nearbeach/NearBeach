from django_otp import user_has_device
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TwoFactorSafeBasicAuthentication(BasicAuthentication):
    """HTTP Basic authentication that never lets a password alone stand in for two-factor authentication

    A user with a two-factor device must sign in through the login page, or use an API token. The refusal is worded
    exactly like a wrong password, so it does not tell anyone the password was right.
    """

    def authenticate_credentials(self, userid, password, request=None):
        user, auth = super().authenticate_credentials(userid, password, request)

        if user_has_device(user):
            raise AuthenticationFailed("Invalid username/password.")

        return user, auth
