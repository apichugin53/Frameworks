from django.contrib.auth import models as auth
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    MODERATOR = "MODERATOR", _("Moderator")
    USER = "USER", _("User")


class User(auth.AbstractUser):
    email = models.EmailField(_("email"), unique=True)
    role = models.CharField(_("role"), max_length=10, choices=Role.choices, default=Role.USER)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to="users/", blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("username",)


class Group(auth.Group):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
