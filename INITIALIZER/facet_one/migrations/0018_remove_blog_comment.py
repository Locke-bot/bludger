# Generated by Django 3.1.1 on 2020-10-15 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0017_blog_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='comment',
        ),
    ]
