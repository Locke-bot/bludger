# Generated by Django 3.1.1 on 2020-11-01 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0018_remove_blog_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
