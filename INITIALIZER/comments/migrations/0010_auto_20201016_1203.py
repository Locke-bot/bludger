# Generated by Django 3.1.1 on 2020-10-16 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20201016_1159'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserCommentReplies',
            new_name='UserCommentReply',
        ),
    ]