from django.contrib.auth import get_user_model
from django.db import models
from song.models import Song


class FavouriteSong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = (("song", "author"),)
