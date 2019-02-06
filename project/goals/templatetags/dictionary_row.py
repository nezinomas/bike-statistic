from django import template

register = template.Library()


@register.simple_tag
def get_row(dict, row_index):
    if row_index in dict:
        r = dict[row_index]
    else:
        r = None
    return r
