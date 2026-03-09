from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DogsConfig(AppConfig):
    name = 'dogs'
    verbose_name = _('Dogs')
