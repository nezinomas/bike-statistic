from django import template

register = template.Library()


@register.simple_tag
def get_row(dict, row_index, return_column_label):
    if row_index in dict:
        r = dict[row_index][return_column_label]
    else:
        r = None

    return r
