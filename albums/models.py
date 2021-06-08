from django.contrib.auth import get_user_model
from django.db import models
from song.models import Song


class Album(models.Model):
    name = models.CharField(max_length=120)
    songs = models.ManyToManyField(Song, through='AlbumsSong')
    owners = models.ManyToManyField(get_user_model())


class AlbumsSong(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True, related_name='tracks')
    add_date = models.DateField(auto_now_add=True, blank=True)
