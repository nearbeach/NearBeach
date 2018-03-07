from django.template import Library
register = Library()


@register.filter(name='mul')
def cut(value, arg):
    return value * arg


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
