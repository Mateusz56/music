from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=120)
    year = models.DateField()
