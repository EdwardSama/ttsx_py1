from django.template import Library

register = Library()

@register.filter
def sub(str):
    list = str.split(' ')
    return list[1]

@register.filter
def sub0(str):
    list = str.split(' ')
    return list[0]