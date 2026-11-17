"""Module providing abstracted class containing the free-form meta_data JSON field"""

from django.db import models


# ABSTRACTED CLASS
class MetaDataAbstraction(models.Model):
    """Class containing the meta_data field for NearBeach's objects.

    meta_data is a JSON object (never a list or scalar) used to store free-form data against an
    object, e.g. by integrations and plugins. Anyone who can read the object can read all of it,
    so it must not hold secrets. Updates through the API are merged, see
    `NearBeach.utils.meta_data.merge_meta_data`.
    """

    meta_data = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        """Meta information for MetaDataAbstraction model"""

        abstract = True
