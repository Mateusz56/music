from django.db import models


class Song(models.Model):

    class Genres(models.TextChoices):
        EIGHTIES = "80s",
        NINETIES = "90s",
        ACOUSTIC = "Acoustic",
        ALTERNATIVE = "Alternative",
        AMBIENT = "Ambient",
        BTS = "Bts",
        COUNTRY = "Country",
        DANCE_PUNK = "Dance punk",
        DOWNTEMPO = "Downtempo",
        ELECTRONIC = "Electronic",
        EMO = "Emo",
        EPIC = "Epic",
        FOLK = "Folk",
        GRUNGE = "Grunge",
        HIPHOP = "Hip-hop",
        INDIE = "Indie",
        INDUSTRIAL = "Industrial",
        BLUNT = "James blunt",
        JAZZ = "Jazz",
        LOFI = "Lo-fi",
        METAl = "Metal",
        METALCORE = "Metalcore",
        POP = "Pop",
        POPPUNK = "Pop punk",
        POSTHARDCORE = "Post-hardcore",
        RAP = "Rap",
        RNB = "Rnb",
        ROCK = "Rock",
        SOUL = "Soul"

    title = models.CharField(max_length=120, null=False)
    performer = models.CharField(max_length=120, default="Unknown")
    year = models.PositiveSmallIntegerField(default=2000, blank=True, null=True)
    genre = models.CharField(max_length=20, choices=Genres.choices, default=Genres.POP)
