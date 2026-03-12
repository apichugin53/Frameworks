from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag()
def media(val):
    if val:
        return f'/media/{val}'
    return '/static/img/no_avatar.png'


@register.simple_tag(name='status_action')
def reverse_is_active_status_as_action(user):
    if user.is_active:
        return _('block')
    return _('unblock')
