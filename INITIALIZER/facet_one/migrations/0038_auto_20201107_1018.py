# Generated by Django 3.1.1 on 2020-11-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0037_urlcount_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlcount',
            name='description',
            field=models.CharField(help_text='link descriptor (homepage, e.t.c)', max_length=50),
        ),
    ]
