from django.conf import settings
from django.db import models
from django.db.models.expressions import F
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Breed(models.Model):
    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(_('description'))

    class Meta:
        verbose_name = _('breed')
        verbose_name_plural = _('breeds')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("dogs:breed_details", kwargs={"pk": self.id})


class DogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('breed')


class Dog(models.Model):
    name = models.CharField(_('dog name'), max_length=64)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name=_('breed'))
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='dogs/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('owner'), on_delete=models.SET_NULL, blank=True, null=True)
    views = models.PositiveIntegerField(_('views'), blank=True, default=0)
    objects = DogManager()

    def __str__(self):
        return f'{self.name} ({self.breed})'

    class Meta:
        verbose_name = _('dog')
        verbose_name_plural = _('dogs')

    def get_absolute_url(self):
        return reverse("dogs:dog_details", kwargs={"pk": self.id})

    def update_views(self, viewer_user):
        if viewer_user != self.owner:
            self.views = F('views') + 1
            self.save()

    def save(
            self,
            *,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        if self.owner and self.views % 100 == 0:
            self.owner.email_user(
                subject=f'{self} added',
                message=f'You have just added {self}',
                fail_silently=False,
            )


class Pedigree(models.Model):
    ancestor = models.ForeignKey(Dog, related_name='descendants', on_delete=models.CASCADE, blank=True,
                                 verbose_name=_('ancestor'))
    descendant = models.ForeignKey(Dog, related_name='ancestors', on_delete=models.CASCADE, blank=True,
                                   verbose_name=_('descendant'))

    class Meta:
        unique_together = (('ancestor', 'descendant'),)
        verbose_name = _('pedigree')
        verbose_name_plural = _('pedigrees')


class Comment(models.Model):
    comment = models.TextField(_('comment'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, verbose_name=_('dog'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=False)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = (Coalesce('updated', 'created').desc(),)

    def save(
            self,
            *,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        if not self._state.adding:
            self.updated = timezone.now()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
