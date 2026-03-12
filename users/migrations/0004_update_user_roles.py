from django.db import migrations
from django.db.models import Case, When
from django.db.models.expressions import Value

from users.models import Role


def update_staff_roles_forward(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).filter(is_staff=True).update(
        role=Case(
            When(is_superuser=True, then=Value(Role.ADMIN)),
            default=Value(Role.MODERATOR)
        )
    )


def update_staff_roles_reverse(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).filter(is_staff=True).update(role=Value(Role.USER))


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_user_role'),
    ]

    operations = [
        migrations.RunPython(update_staff_roles_forward, update_staff_roles_reverse),
    ]
