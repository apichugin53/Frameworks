from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth import models as auth
from django.utils.translation import gettext_lazy as _

from users.models import Group

User = get_user_model()


class MemberAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'role',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'role',
                    'usable_password',
                    'password1',
                    'password2'
                ),
            },
        ),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role',)
    list_filter = ('is_active', 'role', 'is_staff', 'is_superuser',)
    readonly_fields = ('is_staff', 'is_superuser',)


class MemberGroupAdmin(GroupAdmin):
    pass


admin.site.register(User, MemberAdmin)
admin.site.unregister(auth.Group)
admin.site.register(Group, MemberGroupAdmin)
