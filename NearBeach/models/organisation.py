"""Module providing Organisation tables for NearBeach."""

from django.db import models

from NearBeach.models.document.document import Document
from NearBeach.models.abstraction.common_abstractions import CommonInfo


class Organisation(CommonInfo):
    """Class containing fields for Organisation model."""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    profile_picture = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta definition for Organisation model."""

        verbose_name_plural = "Organisations"
        ordering = ["name"]


# ABSTRACTION
class OrganisationForeignKey(models.Model):
    """Class containing abstraction for Organisation"""

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta information for Organisation model"""

        abstract = True
