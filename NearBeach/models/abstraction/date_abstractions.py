"""Module providing abstracted class containing start and end date"""

from django.db import models
from django.conf import settings

# ABSTRACTED CLASS
class DateTimeAbstraction(models.Model):
    """Class containing start and end date fields for NearBeach's models"""
    start_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Meta information for DateAbstraction model"""

        abstract = True
