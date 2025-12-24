"""Module providing enums for objects"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ObjectLinkRelationship(models.TextChoices):
    """Class of enum options for Object Link Relationships"""
    BLOCK = "block", _("Block")
    DUPLICATE = "duplicate", _("Duplicate")
    RELATE = "relate", _("Relate")
    SUBOBJECT = "subobject", _("Subobject")


class ObjectPriority(models.IntegerChoices):
    """Class of enum options for Object Priority"""
    HIGHEST = 0, _("Highest")
    HIGH = 1, _("High")
    NORMAL = 2, _("Normal")
    LOW = 3, _("Low")
    LOWEST = 4, _("Lowest")


class ObjectTemplateType(models.IntegerChoices):
    """Class of enum options for Object Template Type"""
    PROJECT = 0, _("project")
    TASK = 1, _("task")
    KANBAN_CARD = 2, _("kanban_card")
