# Generated by Django 3.1.1 on 2020-10-16 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20201013_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.usercomment'),
        ),
    ]
