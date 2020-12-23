# Generated by Django 3.1.1 on 2020-10-26 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0023_commentlikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
