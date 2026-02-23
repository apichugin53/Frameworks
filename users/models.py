from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
