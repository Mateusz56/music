from django.contrib.auth import get_user_model
from django.db import models
from albums.models import Album


class AlbumComment(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    content = models.TextField()
