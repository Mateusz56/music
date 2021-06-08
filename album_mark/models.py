from django.db import models
from albums.models import Album
from django.contrib.auth import get_user_model


class AlbumMark(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_marks')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField()
