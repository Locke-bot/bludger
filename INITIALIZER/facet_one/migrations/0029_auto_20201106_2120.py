# Generated by Django 3.1.1 on 2020-11-06 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0028_auto_20201106_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linksvisit',
            name='url_visit_count',
        ),
        migrations.AddField(
            model_name='url',
            name='today_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='url',
            name='url_visit_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
