from django.contrib.auth import models as auth
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Q, Case, When, Value
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    MODERATOR = "MODERATOR", _("Moderator")
    USER = "USER", _("User")

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")


class RoleUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.USER)
        return super().create_user(username, email, password, **extra_fields)

    def create_moderator(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", Role.MODERATOR)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class User(auth.AbstractUser):
    email = models.EmailField(_("email"), unique=True)
    role = models.CharField(_("role"), max_length=10, choices=Role.choices, default=Role.USER)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to="users/", blank=True)
    objects = RoleUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

        constraints = [
            models.CheckConstraint(
                condition=Q(
                    role=Case(
                        When(Q(is_staff=True) & Q(is_superuser=True), then=Value(Role.ADMIN)),
                        When(Q(is_staff=True) & Q(is_superuser=False), then=Value(Role.MODERATOR)),
                        default=Value(Role.USER)
                    )
                ),
                name="role_check"
            )
        ]

    def __str__(self):
        return f'{self.username} ({Role(self.role).label})'

    def can_edit_user(self, user_id):
        return self.is_moderator or self.id == user_id

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR or self.is_admin

    def get_absolute_url(self):
        return reverse("users:user_details", kwargs={"pk": self.id})

    def save(
            self,
            *,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.is_staff = self.role == Role.MODERATOR or self.role == Role.ADMIN
        self.is_superuser = self.role == Role.ADMIN
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class Group(auth.Group):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
