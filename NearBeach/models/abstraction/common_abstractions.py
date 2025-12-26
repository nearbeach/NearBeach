"""Module providing abstracted class containing common fields for NearBeach's Models"""

from django.db import models
from django.conf import settings


# ABSTRACTED CLASS
class CommonInfo(models.Model):
    """Class containing common fields for NearBeach's Models"""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    creation_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_creation_user",
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        """Meta information for CommonInfo model"""

        abstract = True












