# Generated by Django 4.1.7 on 2023-06-14 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_userprofile_cover_pic_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
    ]