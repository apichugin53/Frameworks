from django.db import models
from django.utils.translation import gettext_lazy as _


class Breed(models.Model):
    name = models.CharField(_('название'), max_length=64)
    description = models.TextField(_('описание'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('порода')
        verbose_name_plural = _('породы')
        ordering = ('name',)


class Dog(models.Model):
    name = models.CharField(_('кличка'), max_length=64)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name=_('порода'))
    description = models.TextField(_('описание'), blank=True)
    photo = models.ImageField(_('фото'), upload_to='dogs/', null=True)

    def __str__(self):
        return f'{self.breed} {self.name}'

    class Meta:
        verbose_name = _('собака')
        verbose_name_plural = _('собаки')
        ordering = ('name', 'breed',)
