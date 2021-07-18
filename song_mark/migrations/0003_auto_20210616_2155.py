# Generated by Django 3.1.7 on 2021-06-16 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_song_year'),
        ('song_mark', '0002_remove_songmark_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songmark',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_marks', to='song.song'),
        ),
    ]
