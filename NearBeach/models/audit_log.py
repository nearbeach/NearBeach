"""Module providing the Audit Log table for NearBeach"""

from typing import Any

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from NearBeach.utils.enums.audit_enums import AuditAction


class AuditLog(models.Model):
    """
    Append-only record of a change made to an object - who, when, and which fields moved.

    Deliberately NOT a CommonInfo model: rows are never soft deleted or edited. They leave the table only
    through the retention prune (`manage.py prune_audit`) or are scrubbed by the GDPR erasure helpers in
    `AuditService`.
    """

    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # SET_NULL, so deleting a user never deletes history. `username` keeps who it was.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_user",
        blank=True,
        null=True,
    )
    username = models.CharField(max_length=150, blank=True, default="")
    # Destination string, e.g. "project" - the same names the permission decorators use
    object_type = models.CharField(max_length=50)
    object_id = models.BigIntegerField()
    action = models.CharField(max_length=20, choices=AuditAction)
    summary = models.CharField(max_length=255, blank=True, default="")
    # {"field": {"old": ..., "new": ...}}
    changes = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.object_type} {self.object_id}: {self.action}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Rows are append-only - an existing row may not be rewritten through save()"""
        if not self._state.adding:
            raise ValueError("Audit log entries can not be edited")
        super().save(*args, **kwargs)

    class Meta:
        """Meta definition for AuditLog"""

        verbose_name_plural = "Audit Logs"
        ordering = ["-id"]
        indexes = [
            models.Index(
                fields=["object_type", "object_id", "-date_created"],
                name="audit_object_idx",
            ),
            models.Index(fields=["user", "-date_created"], name="audit_user_idx"),
            models.Index(fields=["date_created"], name="audit_created_idx"),
        ]
