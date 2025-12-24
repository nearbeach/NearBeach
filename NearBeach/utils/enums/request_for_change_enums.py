"""Module providing enums for Request for Change models"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class RequestForChangeApproval(models.IntegerChoices):
    """Class containing enums for Request for Change Approvals"""
    WAITING = 1, _('Waiting')
    APPROVED = 2, _('Approved')
    REJECTED = 3, _('Rejected')
    CANCEL = 4, _('Cancel')


class RequestForChangeImpact(models.IntegerChoices):
    """Class containing enums for Request for Change Impact"""
    HIGH = 3, _("High"),
    MEDIUM = 2, _("Medium"),
    LOW = 1, _("Low"),


class RequestForChangePriority(models.IntegerChoices):
    """Class containing enums for Request for Change Priority"""
    CRITICAL = 4, _("Critical")
    HIGH = 3, _("High")
    MEDIUM = 2, _("Medium")
    LOW = 1, _("Low")


class RequestForChangeRisk(models.IntegerChoices):
    """Class containing enums for Request for Change Risk"""
    VERY_HIGH = 5, _("Very High")
    HIGH = 4, _("High")
    MODERATE = 3, _("Moderate")
    LOW = 2, _("Low")
    NONE = 1, _("None")


class RequestForChangeStatus(models.IntegerChoices):
    """Class containing enums for Request for Change Status"""
    DRAFT = 1, _("Draft")
    WAITING_FOR_APPROVAL = 2, _("Waiting for approval")
    APPROVED = 3, _("Approved")
    STARTED = 4, _("Started")
    FINISHED = 5, _("Finished")
    REJECTED = 6, _("Rejected")
    PAUSED = 7, _("Paused")
    READY_FOR_QA = 8, _("Ready for QA")
    FAILED = 9, _("Failed")


class RequestForChangeType(models.IntegerChoices):
    """Class containing enums for Request for Change Type"""
    EMERGENCY = 4, _("Emergency")
    HIGH = 3, _("High")
    MEDIUM = 2, _("Medium")
    LOW = 1, _("Low")
