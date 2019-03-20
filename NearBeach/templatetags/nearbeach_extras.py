import datetime, pytz
from django.utils import timezone
from django.conf import settings
from django.template import Library
register = Library()


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