from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth import models as auth

from users.models import Group

User = get_user_model()


class MemberAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'usable_password',
                    'password1',
                    'password2'
                ),
            },
        ),
    )


class MemberGroupAdmin(GroupAdmin):
    pass


admin.site.register(User, MemberAdmin)
admin.site.unregister(auth.Group)
admin.site.register(Group, MemberGroupAdmin)
