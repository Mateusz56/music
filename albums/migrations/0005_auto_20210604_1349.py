# Generated by Django 3.1.5 on 2021-06-04 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_song_year'),
        ('albums', '0004_album_owners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumssong',
            name='add_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='albumssong',
            name='song',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='song.song'),
        ),
    ]
