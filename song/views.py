from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from song.serializer import SongSerializer
from song.models import Song
from rest_framework import permissions
from django.db.models import Q
from datetime import datetime

class SongList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        songs = Song.objects.all()
        if 'name' in request.query_params:
            songs = Song.objects.filter(Q(title__contains=request.query_params.get('name')) | Q(performer__contains=request.query_params.get('name')))
        if 'genres' in request.query_params:
            songs = songs.filter(genre__in=request.query_params.get('genres').split(','))
        if 'yearSince' in request.query_params:
            songs = songs.filter(year__gte=request.query_params.get('yearSince'))
        if 'yearTo' in request.query_params:
            songs = songs.filter(year__lte=request.query_params.get('yearTo'))
        if 'offset' in request.query_params:
            offset = int(request.query_params.get('offset'))
        else:
            offset = 0
        songs = songs[offset: offset + 20]

        print(songs.query)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenresList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        data = Song.Genres.labels
        return Response(data)
# import requests
# word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
# response = requests.get(word_site)
# WORDS = response.content.splitlines()
#
# from song.models import Song
# import random
# for i in range(0, 100):
#     performer = random.choice(WORDS)
#     for j in range(0, 20):
#         s = Song(title = random.choice(WORDS), performer=performer, year=datetime.now(), genre = random.choice(Song.Genres.choices))
#         s.save()