# Generated by Django 3.1.1 on 2020-11-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facet_one', '0021_auto_20201102_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images'),
        ),
        migrations.DeleteModel(
            name='FlatPageForm',
        ),
    ]