from django.db import models



class Song(models.Model):

    class Genres(models.TextChoices):
        POP = 'Pop',
        ROCK = 'Rock',
        FOLK = 'Folk',
        METAL = 'Metal',
        OTHER = 'Other'

    title = models.CharField(max_length=120, null=False)
    performer = models.CharField(max_length=120, default="Unknown")
    year = models.DateField()
    genre = models.CharField(max_length=20, choices=Genres.choices, default=Genres.OTHER)
