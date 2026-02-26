from django.db import models
from django.utils.translation import gettext_lazy as _


class Breed(models.Model):
    name = models.CharField(_('breed name'), max_length=64)
    description = models.CharField(_('description'), max_length=256)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('breed')
        verbose_name_plural = _('breeds')
        ordering = ('name',)


class Dog(models.Model):
    name = models.CharField(_('dog name'), max_length=64)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    photo = models.ImageField(_('photo'), upload_to='dogs/', null=True)

    def __str__(self):
        return f'{self.breed} {self.name}'

    class Meta:
        verbose_name = _('dog')
        verbose_name_plural = _('dogs')
        ordering = ('name', 'breed',)
