from django.shortcuts import render
from rest_framework import generics, permissions

from favourite_album.models import FavouriteAlbum
from favourite_album.serializer import FavouriteAlbumSerializer


class FavouriteAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = FavouriteAlbum.objects.all()
    serializer_class = FavouriteAlbumSerializer


class FavouriteAlbumList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = FavouriteAlbum.objects.all()
    serializer_class = FavouriteAlbumSerializer
