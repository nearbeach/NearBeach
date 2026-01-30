"""Module providing the Authentication views for NearBeach"""
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class ResetPasswordView(View):
    """Class handling authentication"""

    @staticmethod
    def _get_user(uid):
        """Method for retrieving a user by uid"""
        udi_bytes = urlsafe_base64_decode(uid)
        user_id = force_str(udi_bytes)

        return User.objects.filter(
            pk=user_id,
            is_active=True,
        ).first()

    def get(self, request, *args, **kwargs):
        """Method handling GET request for reset password."""
        uid = request.GET.get('uid', None)
        token = request.GET.get('token', None)

        # Check uid and token exist
        if uid is None or token is None:
            return HttpResponseRedirect(reverse("login"))

        # Check that uid is valid
        user = self._get_user(uid)
        if user is None:
            return HttpResponseRedirect(reverse("login"))

        # Validate the token
        is_token_valid = PasswordResetTokenGenerator().check_token(user, token)
        if not is_token_valid:
            return HttpResponseRedirect(reverse("login"))

        return render(request, "NearBeach/authentication/authentication.html")
