"""Module providing Customer tables for NearBeach"""

from django.db import models

from NearBeach.models.document.document import Document
from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.organisation import Organisation


class ListOfTitle(CommonInfo):
    """Class containing List Of Title fields."""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=10)

    def __str__(self):
        return str(self.title)

    class Meta:
        """Meta definition for ListOfTitle."""

        verbose_name_plural = "List Of Titles"
        ordering = ["title"]


class Customer(CommonInfo):
    """Class containing Customer fields"""

    id = models.BigAutoField(primary_key=True)
    title = models.ForeignKey(
        ListOfTitle,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    profile_picture = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(str(self.id) + " - " + self.first_name + " " + self.last_name)

    class Meta:
        """Meta information for Customers model"""

        verbose_name_plural = "Customers"
        ordering = ["last_name", "first_name"]


# ABSTRACTION
class CustomerForeignKey(models.Model):
    """Class containing fields for CustomerForeignKey table"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta information for CustomerForeignKey model"""

        abstract = True
