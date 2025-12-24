"""Module providing group tables for NearBeach"""

from django.db import models

from NearBeach.models.field.common_info import CommonInfo


class Group(CommonInfo):
    """Class containing fields for group table"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=50,
    )
    parent_group = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def natural_key(self):
        return self.id, self.name

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta definitions for Group"""

        verbose_name_plural = "Groups"
