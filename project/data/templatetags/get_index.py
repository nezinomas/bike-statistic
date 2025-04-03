from django import template

register = template.Library()


@register.filter
def get_index(arr, i):
    return arr[i]
