from django.db import models
from song.models import Song


class Album(models.Model):
    name = models.CharField(max_length=120)
    songs = models.ManyToManyField(Song)
