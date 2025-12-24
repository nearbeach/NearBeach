"""Module providing Customer tables for NearBeach"""

from django.db import models

from NearBeach.models.document.document import Document
from NearBeach.models.field.common_info import CommonInfo
from NearBeach.models.organisation.organisation import Organisation


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

    customer_id = models.BigAutoField(primary_key=True)
    customer_title = models.ForeignKey(
        ListOfTitle,
        on_delete=models.CASCADE,
    )
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=200)
    customer_profile_picture = models.ForeignKey(
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
        return str(
            str(self.customer_id)
            + " - "
            + self.customer_first_name
            + " "
            + self.customer_last_name
        )

    class Meta:
        """Meta information for Customers model"""

        verbose_name_plural = "Customers"
        ordering = ["customer_first_name"]
