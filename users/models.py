from django.contrib.auth import models as auth
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Q, Case, When, Value
from django.template.loader import render_to_string
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
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", Role.USER)
        return super().create_superuser(username, email, password, **extra_fields)

    def create_moderator(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", Role.MODERATOR)
        return super().create_superuser(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
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
        need_send_email = self._state.adding
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        if need_send_email:
            message = render_to_string('security/registration_email.html', {
                'username': self.username,
                'url': self.get_absolute_url(),
            })
            self.email_user(
                subject=f'Registration',
                message=message,
                fail_silently=False,
            )

    # def save(self, **kwargs):
    #     super().save(**kwargs)

    def can_edit_user(self, user):
        return self == user or self.is_moderator


class Group(auth.Group):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
