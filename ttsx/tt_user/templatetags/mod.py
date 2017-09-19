from django.template import Library

register = Library()


@register.filter
def cheng(a,b):
    return a*b