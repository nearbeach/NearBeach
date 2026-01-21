from django.db import models
from django.utils.translation import gettext_lazy as _


class LoginStatusEnum(models.TextChoices):
    """Class of enum options for Login status"""

    INCORRECT_LOGIN = "incorrect_login", _("Incorrect login")
    SUCCESS = "success", _("Success")
    FAILURE = "failure", _("Failure")
    TWO_FACTOR_REQUIRED = "two_factor_required", _("Two-Factor Required")
