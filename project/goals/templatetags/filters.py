from django import template

register = template.Library()


@register.filter
def duration(duration):
    total_seconds = int(duration)
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    return '{h:02d}:{m:02d}:{s:02d}'.format(h=h, m=m, s=s)
