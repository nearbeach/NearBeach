"""Hardening for the Django admin login, which sits outside NearBeach's own login page

The admin login is a second way in with a username and password - so it gets the same two protections as the main
login: the auth rate limits, and the two-factor code for anyone who has set up two-factor authentication.
"""

from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django_otp import match_token, user_has_device
from django_otp.plugins.otp_email.models import EmailDevice

from NearBeach.utils.throttle.AuthHourThrottle import AuthHourThrottle
from NearBeach.utils.throttle.AuthMinuteThrottle import AuthMinuteThrottle


class AdminLoginMinuteThrottle(AuthMinuteThrottle):
    """The login throttle, counted per address even when someone is already signed in as a normal user"""

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": f"admin_{self.scope}", "ident": self.get_ident(request)}


class AdminLoginHourThrottle(AuthHourThrottle):
    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": f"admin_{self.scope}", "ident": self.get_ident(request)}


class SecureAdminAuthenticationForm(AdminAuthenticationForm):
    """The admin login form, asking for the two-factor code when the user has one set up"""

    otp_token = forms.CharField(
        required=False,
        label="Two-factor code",
        widget=forms.TextInput(attrs={"autocomplete": "one-time-code"}),
    )

    def clean(self):
        cleaned_data = super().clean()  # Checks the password - raises if it is wrong
        user = self.get_user()

        if user is not None and user_has_device(user):
            token = (cleaned_data.get("otp_token") or "").strip()
            if not token:
                # An email device can only be checked once it has sent a code
                email_device = EmailDevice.objects.filter(user=user, confirmed=True).first()
                if email_device is not None:
                    email_device.generate_challenge()
                raise ValidationError("Enter your two-factor code.", code="otp_required")

            if match_token(user, token) is None:
                raise ValidationError("That two-factor code is not valid.", code="otp_invalid")

        return cleaned_data


def harden_admin_site(site) -> None:
    """Put the throttle and the two-factor check in front of the given admin site's login"""
    site.login_form = SecureAdminAuthenticationForm
    site.login_template = "NearBeach/admin/login.html"

    original_login = site.login

    def login(request, extra_context=None):
        if request.method == "POST":
            for throttle in (AdminLoginMinuteThrottle(), AdminLoginHourThrottle()):
                if not throttle.allow_request(request, None):
                    return HttpResponse(
                        "Too many login attempts. Please wait a while and try again.",
                        status=429,
                        content_type="text/plain",
                    )

        return original_login(request, extra_context)

    site.login = login
