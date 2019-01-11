from django import template

register = template.Library()


@register.inclusion_tag('bikes/includes/button_delete.html')
def button_delete(pk, *args, **kwargs):
    return {
        'pk': pk
    }


@register.inclusion_tag('bikes/includes/button_update.html')
def button_update(pk, *args, **kwargs):
    return {
        'pk': pk
    }


@register.inclusion_tag('bikes/includes/button_close.html')
def button_close(pk, *args, **kwargs):
    return {
        'pk': pk
    }
