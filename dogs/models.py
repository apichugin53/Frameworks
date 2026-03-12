from django.core.mail import send_mail
from django.db import models
from django.db.models.expressions import F
from django.utils.translation import gettext_lazy as _

from webapp import settings


class Breed(models.Model):
    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(_('description'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('breed')
        verbose_name_plural = _('breeds')
        ordering = ('name',)


class Dog(models.Model):
    name = models.CharField(_('dog name'), max_length=64)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name=_('breed'))
    birth_date = models.DateField(_('birth date'), null=True)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='dogs/', null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('owner'))
    views = models.PositiveIntegerField(_('views'), default=0)

    def __str__(self):
        return f'{self.breed} {self.name}'

    class Meta:
        verbose_name = _('dog')
        verbose_name_plural = _('dogs')
        ordering = ('name', 'breed',)

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
            send_mail(
                subject=f'{self.breed} {self.name} views',
                message=f'You have {self.views} views for {self}',
                from_email='noreply@example.com',
                recipient_list=['%s' % self.owner.email],
                fail_silently=False,
            )


class Pedigree(models.Model):
    ancestor = models.ForeignKey(Dog, related_name='descendants', on_delete=models.CASCADE, verbose_name=_('ancestor'))
    descendant = models.ForeignKey(Dog, related_name='ancestors', on_delete=models.CASCADE,
                                   verbose_name=_('descendant'))

    class Meta:
        unique_together = (('ancestor', 'descendant'),)
        verbose_name = _('pedigree')
        verbose_name_plural = _('pedigrees')
