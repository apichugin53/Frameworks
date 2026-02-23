from django.db import models
from accounts.models import CustomUser

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название породы')
    description = models.TextField(blank=True, verbose_name='Описание')
    size = models.CharField(
        max_length=20,
        choices=[
            ('small', 'Маленькая'),
            ('medium', 'Средняя'),
            ('large', 'Большая'),
        ],
        verbose_name='Размер'
    )

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кличка')
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        verbose_name='Порода'
    )
    age = models.PositiveIntegerField(verbose_name='Возраст')
    color = models.CharField(max_length=50, verbose_name='Окрас')
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Вес (кг)'
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    photo = models.ImageField(
        upload_to='dogs_photos/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    def __str__(self):
        return f'{self.name} ({self.breed.name})'
