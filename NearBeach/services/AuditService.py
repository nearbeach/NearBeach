"""Service that records, reads, prunes and scrubs the audit log"""

from datetime import timedelta
from typing import Any, Dict, Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from NearBeach.models.audit_log import AuditLog
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
)
from NearBeach.utils.enums.audit_enums import AuditAction
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus

# Bookkeeping fields CommonInfo maintains - the audit row already says who and when
EXCLUDED_FIELDS = {
    "id",
    "date_created",
    "date_modified",
    "change_user",
    "creation_user",
    "is_deleted",
}

# Any field whose name contains one of these is stored as MASKED. Everything else is logged
SECRET_MARKERS = ("password", "token", "secret", "api_key", "private_key")
MASKED = "***"

# Snapshot of an object's logged fields - {field name: raw value}. Foreign keys hold the id.
Snapshot = Dict[str, Any]


class AuditService:
    """
    Writes diffs of object changes into AuditLog.

    Call it from the object's service, inside the same `transaction.atomic()` as the change itself, so the
    change and its audit row commit (or roll back) together:

        before = AuditService.snapshot(project)
        serializer.save(change_user=request.user)
        AuditService.record_update(request, "project", before, project)
    """

    # --- snapshots and diffs -------------------------------------------------------------------------------

    @staticmethod
    def snapshot(instance: models.Model) -> Snapshot:
        """Raw values of every logged field. Reads only attributes already on the instance - no queries"""
        return {
            field.name: getattr(instance, field.attname)
            for field in instance._meta.concrete_fields
            if field.name not in EXCLUDED_FIELDS
        }

    @staticmethod
    def _label(instance: models.Model, field_name: str, value: Any) -> Any:
        """Readable value for a changed foreign key (e.g. the status title), the raw id if it can not be found"""
        if value is None:
            return None

        field = instance._meta.get_field(field_name)
        if not isinstance(field, models.ForeignKey):
            return value

        related = field.related_model._base_manager.filter(pk=value).first()
        return str(related) if related is not None else value

    @staticmethod
    def _mask(field_name: str, value: Any) -> Any:
        if any(marker in field_name.lower() for marker in SECRET_MARKERS):
            return MASKED if value not in (None, "") else value
        return value

    @classmethod
    def diff(
        cls, before: Snapshot, after: Snapshot, instance: models.Model
    ) -> Dict[str, Dict[str, Any]]:
        """Only the fields that changed, as {field: {"old": ..., "new": ...}}"""
        changes: Dict[str, Dict[str, Any]] = {}
        for name, new_value in after.items():
            old_value = before.get(name)
            if old_value == new_value:
                continue

            old_logged, new_logged = old_value, new_value
            # Only the changed foreign keys cost a lookup
            if isinstance(instance._meta.get_field(name), models.ForeignKey):
                old_logged = cls._label(instance, name, old_value)
                new_logged = cls._label(instance, name, new_value)

            changes[name] = {
                "old": cls._mask(name, old_logged),
                "new": cls._mask(name, new_logged),
            }
        return changes

    # --- writing -------------------------------------------------------------------------------------------

    @staticmethod
    def _ip_address(request: AuthenticatedRequest) -> Optional[str]:
        meta = getattr(request, "META", {}) or {}
        return meta.get("REMOTE_ADDR") or None

    @classmethod
    def record(
        cls,
        request: AuthenticatedRequest,
        destination: str,
        object_id: ObjectId,
        action: str,
        changes: Optional[Dict[str, Dict[str, Any]]] = None,
        summary: str = "",
    ) -> AuditLog:
        """Write one audit row"""
        return AuditLog.objects.create(
            user=request.user,
            username=request.user.get_username(),
            object_type=destination,
            object_id=int(object_id),
            action=action,
            summary=str(summary)[:255],
            changes=changes or {},
            ip_address=cls._ip_address(request),
        )

    @classmethod
    def record_create(
        cls, request: AuthenticatedRequest, destination: str, instance: models.Model
    ) -> AuditLog:
        """Log a new object - every field starts from nothing"""
        changes = {
            name: {"old": None, "new": cls._mask(name, value)}
            for name, value in cls.snapshot(instance).items()
        }
        return cls.record(
            request, destination, instance.pk, str(AuditAction.CREATE), changes, str(_("Created"))
        )

    @classmethod
    def record_update(
        cls,
        request: AuthenticatedRequest,
        destination: str,
        before: Snapshot,
        instance: models.Model,
    ) -> Optional[AuditLog]:
        """
        Log the difference between `before` (taken ahead of the save) and the instance now.
        Returns None, and writes nothing, when no logged field changed.
        """
        changes = cls.diff(before, cls.snapshot(instance), instance)
        if not changes:
            return None

        action: str = str(AuditAction.UPDATE)
        summary = str(_("Updated"))

        # Closing is the change people most want to find, so name it
        if "status" in changes:
            action = str(AuditAction.STATUS_CHANGE)
            summary = str(_("Status changed"))
            new_status = getattr(instance, "status", None)
            if (
                getattr(new_status, "higher_order_status", None)
                == ObjectHigherOrderStatus.CLOSED
            ):
                action = str(AuditAction.CLOSE)
                summary = str(_("Closed"))

        return cls.record(request, destination, instance.pk, action, changes, summary)

    @classmethod
    def record_delete(
        cls, request: AuthenticatedRequest, destination: str, object_id: ObjectId
    ) -> AuditLog:
        """Log a (soft) delete"""
        return cls.record(
            request, destination, object_id, str(AuditAction.DELETE), {}, str(_("Deleted"))
        )

    # --- reading -------------------------------------------------------------------------------------------

    @staticmethod
    def get_list(destination: str, object_id: ObjectId) -> QuerySet[AuditLog]:
        """Audit entries for one object, newest first"""
        return AuditLog.objects.filter(
            object_type=destination,
            object_id=int(object_id),
        ).order_by("-date_created", "-id")

    # --- retention and GDPR --------------------------------------------------------------------------------

    @staticmethod
    def prune(days: int) -> int:
        """Delete entries older than `days`. Returns the number removed"""
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _unused = AuditLog.objects.filter(date_created__lt=cutoff).delete()
        return deleted

    @staticmethod
    def scrub_object(destination: str, object_id: ObjectId) -> int:
        """
        Erase the recorded values for one object (e.g. a customer who asked to be forgotten). The rows stay, so
        the fact that something happened is kept, but every field value is gone.
        """
        return AuditLog.objects.filter(
            object_type=destination,
            object_id=int(object_id),
        ).update(changes={}, summary=str(_("Personal data erased")))

    @staticmethod
    def anonymise_user(user: User) -> int:
        """Remove who-did-it details for one user from every entry they made"""
        return AuditLog.objects.filter(user=user).update(
            user=None, username=str(_("erased user")), ip_address=None
        )
