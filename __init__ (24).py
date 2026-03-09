from django.contrib import admin

from users.models import User

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active")

admin.site.register(User, MemberAdmin)
