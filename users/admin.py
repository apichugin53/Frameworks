from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        ('Additional Info', {'fields': ('custom_field',)}),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)