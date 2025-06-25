from django.db import models
from django.utils.translation import gettext_lazy as _


class ObjectPriority(models.IntegerChoices):
    HIGHEST = 0, _("Highest")
    HIGH = 1, _("High")
    NORMAL = 2, _("Normal")
    LOW = 3, _("Low")
    LOWEST = 4, _("Lowest")