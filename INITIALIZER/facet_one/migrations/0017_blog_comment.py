# Generated by Django 3.1.1 on 2020-10-15 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0016_remove_blog_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]