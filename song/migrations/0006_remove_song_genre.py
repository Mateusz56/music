# Generated by Django 3.1.7 on 2021-12-27 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_song_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='genre',
        ),
    ]
