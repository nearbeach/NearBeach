from django.db import models
from django.utils.translation import gettext_lazy as _


class RequestForChangeImpact(models.IntegerChoices):
    HIGH = 3, _("High"),
    MEDIUM = 2, _("Medium"),
    LOW = 1, _("Low"),


class RequestForChangePriority(models.IntegerChoices):
    CRITICAL = 4, _("Critical")
    HIGH = 3, _("High")
    MEDIUM = 2, _("Medium")
    LOW = 1, _("Low")


class RequestForChangeRisk(models.IntegerChoices):
    VERY_HIGH = 5, _("Very High")
    HIGH = 4, _("High")
    MODERATE = 3, _("Moderate")
    LOW = 2, _("Low")
    NONE = 1, _("None")


class RequestForChangeStatus(models.IntegerChoices):
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
    EMERGENCY = 4, _("Emergency")
    HIGH = 3, _("High")
    MEDIUM = 2, _("Medium")
    LOW = 1, _("Low")
