# Generated by Django 3.1.7 on 2021-04-05 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0002_auto_20210405_2003'),
        ('albums', '0002_remove_album_songs'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumsSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField()),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.album')),
                ('song', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='song.song')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(through='albums.AlbumsSong', to='song.Song'),
        ),
    ]
