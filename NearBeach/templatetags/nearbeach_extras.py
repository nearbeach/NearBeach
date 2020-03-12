import datetime, pytz
from django.utils import timezone
from django.conf import settings
from django.template import Library
register = Library()

#Import data
from NearBeach.models import *


@register.filter(name='filter_assigned_project')
def filter_assigned_project(value,arg):
    """

    :param value: Use "object_assignment" table
    :param arg: What task ID are we focusing on
    :return:
    """
    return value.filter(
        project_id__isnull=False,
        task_id=arg,
    )


@register.filter(name='filter_assigned_task')
def filter_assigned_task(value,arg):
    """

    :param value:
    :param arg:
    :return:
    """
    return value.filter(
        task_id__isnull=False,
        project_id=arg,
    )

@register.filter(name='filter_level_cards')
def filter_level_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the co-ordinates [column,level]
    :return: the filtered python object
    """
    return value.filter(kanban_level=arg)


@register.filter(name='filter_column_cards')
def filter_column_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the co-ordinates [column,level]
    :return: the filtered python object
    """
    return value.filter(kanban_column=arg)



@register.filter(name='filter_requirement_items')
def filter_requirement_items(value,arg):
    """
    :param value: this is the python object being passed through
    :param arg: this is the requirement_id we will filter by
    :return: the filtered python object
    """
    return value.filter(
        is_deleted="FALSE",
    )

@register.filter(name='filter_requirement_item_cards')
def filter_requirement_item_cards(value, arg):
    """
    :param value: this is the python object being passed through
    :param arg: these are the stages of the requirement_item ['draft']
    :return: the filtered python object i.e. ['draft']
    """
    return value.filter(requirement_item_status=arg)

@register.filter
def hours_ago(time, hours):
    """
    :param time:
    :param hours:
    :return:
    """
    location = pytz.timezone(settings.TIME_ZONE)
    local_time = location.localize(datetime.datetime.now())

    try:
        return local_time - time > -datetime.timedelta(hours=hours)
    except:
        return datetime.datetime.now() - time > -datetime.timedelta(hours=hours)


@register.filter
def in_future(time, hours):
    """
    :param time:
    :param hours:
    :return:
    """
    location = pytz.timezone(settings.TIME_ZONE)
    local_time = location.localize(datetime.datetime.now())

    try:
        return local_time + datetime.timedelta(hours=hours) < time
    except:
        return False


@register.filter
def task_related_groups(task_id):
    """

    :param task_id:
    :return:
    """
    group_results = group.objects.filter(
        is_deleted="FALSE",
        group_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            task_id=task_id,
            group_id__isnull=False,
        ).values('group_id')
    )
    return group_results