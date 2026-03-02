from django import template


register = template.Library()


@register.simple_tag()
def media(val):
    if val:
        return f'/media/{val}'
    return '/static/img/logo.svg'
