from django.template import Library
register = Library()


@register.filter(name='mul')
def cut(value, arg):
    return value * arg