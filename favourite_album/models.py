from django.contrib.auth import get_user_model
from django.db import models
from albums.models import Album


class FavouriteAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = (("album", "author"),)
