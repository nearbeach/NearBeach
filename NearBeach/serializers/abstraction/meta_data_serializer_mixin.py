"""Serializer mixin adding the `meta_data` JSON field with merge-patch semantics."""

from typing import Any

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from NearBeach.utils.meta_data import (
    META_DATA_MAX_BYTES,
    MetaData,
    merge_meta_data,
    meta_data_size,
)


class MetaDataSerializerMixin(serializers.Serializer):
    """Adds `meta_data` to a ModelSerializer whose model uses `MetaDataAbstraction`.

    Usage: put it first in the bases and add "meta_data" to `Meta.fields`.

    - The value must be a JSON object, and the *result* of the merge must be at most
      `META_DATA_MAX_BYTES` once serialised.
    - Create stores the value with `null` keys dropped.
    - Update merges into the stored value (JSON Merge Patch, RFC 7386): see `merge_meta_data`.
    """

    meta_data = serializers.JSONField(
        required=False,
        help_text=_(
            "A JSON object of free-form data. Updates are merged into the stored object; "
            "set a key to null to delete it."
        ),
    )

    def validate_meta_data(self, value: Any) -> MetaData:
        if not isinstance(value, dict):
            raise serializers.ValidationError(_("meta_data must be a JSON object."))

        current: MetaData = {}
        if self.instance is not None and isinstance(self.instance, models.Model):
            current = getattr(self.instance, "meta_data", None) or {}

        merged = merge_meta_data(current, value)
        self._check_size(merged)

        if self.instance is None:
            # Create: nothing to merge into, so store the patch with null keys dropped
            return merged

        return value

    @staticmethod
    def _check_size(merged: MetaData) -> None:
        if meta_data_size(merged) > META_DATA_MAX_BYTES:
            raise serializers.ValidationError(
                _("meta_data must be %(limit)s bytes or smaller once saved.") % {"limit": META_DATA_MAX_BYTES}
            )

    def update(self, instance: models.Model, validated_data: dict[str, Any]) -> Any:
        if "meta_data" not in validated_data:
            return super().update(instance, validated_data)

        patch: MetaData = validated_data["meta_data"]

        with transaction.atomic():
            # Re-read under a row lock so two simultaneous patches to different keys both survive
            # (select_for_update is a no-op on SQLite)
            locked: Any = type(instance)._default_manager.select_for_update().get(pk=instance.pk)
            merged = merge_meta_data(locked.meta_data or {}, patch)
            self._check_size(merged)

            validated_data["meta_data"] = merged
            return super().update(instance, validated_data)
