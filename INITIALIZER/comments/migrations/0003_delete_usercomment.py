# Generated by Django 3.1.1 on 2020-10-13 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20201013_1648'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserComment',
        ),
    ]
