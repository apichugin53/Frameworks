from django import template

from webapp import settings

register = template.Library()


@register.simple_tag()
def media(val):
    if val:
        return f'/media/{val}'
    return '/static/img/logo.svg'


@register.simple_tag
def get_languages():
    return settings.LANGUAGES
