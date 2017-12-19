from django import template

register = template.Library()


@register.filter()
def mult(value, arg):
    if not value:
        value = 1
    res = float(value) * float(arg)
    return res
