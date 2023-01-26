from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(str(key), 0.0)


@register.filter
def join(var1, var2):
    return f'{var1}{var2}'
