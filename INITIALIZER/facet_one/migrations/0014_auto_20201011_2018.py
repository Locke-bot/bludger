# Generated by Django 3.1.1 on 2020-10-11 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0013_auto_20201011_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='last_update',
            new_name='last_updated',
        ),
    ]
