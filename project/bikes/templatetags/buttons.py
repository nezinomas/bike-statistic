from django import template

register = template.Library()


@register.inclusion_tag('bikes/includes/button_delete.html')
def button_delete(*args, **kwargs):
    return {
        'pk': kwargs['pk'] if 'pk' in kwargs else '',
        'url': kwargs['url'] if 'url' in kwargs else '',
        'tbl': kwargs['tbl'] if 'tbl' in kwargs else '',
        'type': kwargs['type']
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


@register.inclusion_tag('bikes/includes/button_edit.html')
def button_edit(*args, **kwargs):
    return {
        'pk': kwargs['pk'],
        'url': kwargs['url'],
        'tbl': kwargs['tbl']
    }


@register.inclusion_tag('bikes/includes/button_create.html')
def button_create(*args, **kwargs):
    return {
        'url': kwargs['url'],
        'label': kwargs['label'],
        'tbl': kwargs['tbl'],
        'width': kwargs['width'] if 'width' in kwargs else None
    }
