"""Module providing the Authentication views for NearBeach"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from NearBeach.utils.api.get_user_from_uid import get_user_from_uid


class ResetPasswordView(View):
    """Class handling authentication"""

    def get(self, request, *args, **kwargs):
        """Method handling GET request for reset password."""
        uid = request.GET.get("uid", None)
        token = request.GET.get("token", None)

        # Check uid and token exist
        if uid is None or token is None:
            return HttpResponseRedirect(reverse("login"))

        # Check that uid is valid
        user = get_user_from_uid(uid)
        if user is None:
            return HttpResponseRedirect(reverse("login"))

        # Validate the token
        is_token_valid = PasswordResetTokenGenerator().check_token(user, token)
        if not is_token_valid:
            return HttpResponseRedirect(reverse("login"))

        return render(request, "NearBeach/authentication/authentication.html")
