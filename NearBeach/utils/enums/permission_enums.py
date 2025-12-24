"""Module providing permission enums for NearBeach."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class PermissionLevel(models.IntegerChoices):
    """Class containing enums for Permission Level"""

    NO_PERMISSION = 0, _("No Permission")
    READ_ONLY = 1, _("Read Only")
    EDIT_ONLY = 2, _("Edit Only")
    ADD_AND_EDIT = 3, _("Add and Edit")
    FULL_PERMISSION = 4, _("Full Permission")


class PermissionBoolean(models.IntegerChoices):
    """Class containing enums for Permission Boolean"""

    NO_PERMISSION = 0, _("No Permission")
    HAS_PERMISSION = 1, _("Has Permission")
