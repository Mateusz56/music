from django.db import models
from song.models import Song
from django.contrib.auth import get_user_model


class SongMark(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_marks')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField()
