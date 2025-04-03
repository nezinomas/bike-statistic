from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), 0.0) if dictionary else None


@register.filter
def join(var1, var2):
    return f"{var1}{var2}"


@register.simple_tag
def to_list(*args):
    return args
