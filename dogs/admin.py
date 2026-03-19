from django.contrib import admin

from dogs.models import Breed, Dog


class BreedAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed')
    list_filter = ('breed',)
    ordering = ('name',)


admin.site.register(Breed, BreedAdmin)
admin.site.register(Dog, DogAdmin)
