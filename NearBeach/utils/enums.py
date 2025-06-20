from django.db import models
from django.utils.translation import gettext_lazy as _


class ObjectPriority(models.IntegerChoices):
    HIGHEST = 0, _("Highest")
    HIGH = 1, _("High")
    NORMAL = 2, _("Normal")
    LOW = 3, _("Low")
    LOWEST = 4, _("Lowest")


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
