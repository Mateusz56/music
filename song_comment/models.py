from django.db import models
from song.models import Song
from django.contrib.auth import get_user_model


class SongComment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.TextField()
