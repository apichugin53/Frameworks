from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone number"), max_length=20, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to="users/", blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("username",)