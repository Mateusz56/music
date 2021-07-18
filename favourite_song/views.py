from favourite_song.models import FavouriteSong
from favourite_song.serializer import FavouriteSongSerializer
from rest_framework import generics, permissions


class FavouriteSongDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = FavouriteSong.objects.all()
    serializer_class = FavouriteSongSerializer


class FavouriteSongList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = FavouriteSong.objects.all()
    serializer_class = FavouriteSongSerializer
