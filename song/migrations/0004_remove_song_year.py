# Generated by Django 3.1.7 on 2021-05-28 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0003_auto_20210528_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='year',
        ),
    ]
