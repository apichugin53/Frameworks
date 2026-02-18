from django.contrib import admin

from users.models import User

class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "birthday")

admin.site.register(User, MemberAdmin)
