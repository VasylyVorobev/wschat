from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def set_superuser(apps, schema_editor):
    user_obj = apps.get_model("main", "User")
    user = user_obj(
        email=settings.SUPERUSER_EMAIL,
        first_name='Super',
        last_name='Admin',
        is_staff=True,
        is_active=True,
        is_superuser=True,
        password=make_password(settings.SUPERUSER_PASSWORD)
    )
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_superuser),
    ]
