# Generated by Django 3.1.1 on 2020-10-17 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0014_auto_20201017_0018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercomment',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='usercommentreply',
            options={'default_permissions': ('add',)},
        ),
    ]
