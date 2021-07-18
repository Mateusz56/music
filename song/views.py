from django.db.models.expressions import RawSQL
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from albums.models import Album
from favourite_song.models import FavouriteSong
from song.serializer import SongSerializer
from song.models import Song
from rest_framework import permissions
from django.db.models import Q, F, Subquery, Avg
import json


class SongList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        songs = Song.objects.all()

        if 'albumId' in request.query_params:
            songs = Album.objects.get(id=request.query_params.get('albumId')).songs.all()
        if 'name' in request.query_params:
            songs = Song.objects.filter(Q(title__contains=request.query_params.get('name')) | Q(performer__contains=request.query_params.get('name')))
        if 'genres' in request.query_params:
            songs = songs.filter(genre__in=request.query_params.get('genres').split(','))
        if 'yearSince' in request.query_params:
            songs = songs.filter(year__gte=request.query_params.get('yearSince'))
        if 'yearTo' in request.query_params:
            songs = songs.filter(year__lte=request.query_params.get('yearTo'))

        songs = songs.annotate(marks_avg=Avg('song_marks__mark'))
        if 'mark' in request.query_params:
            mark_filter = request.query_params.get('mark_filter')
            if mark_filter == 'lte':
                songs = songs.filter(marks_avg__lte=request.query_params.get('mark'))
            elif mark_filter == 'gte':
                songs = songs.filter(marks_avg__gte=request.query_params.get('mark'))
            elif mark_filter == 'exact':
                songs = songs.filter(marks_avg=request.query_params.get('mark'))
            elif mark_filter == 'gt':
                songs = songs.filter(marks_avg__gt=request.query_params.get('mark'))
            elif mark_filter == 'lt':
                songs = songs.filter(marks_avg__lt=request.query_params.get('mark'))

        if 'user' in request.query_params:
            #songs = songs.annotate(favourite=RawSQL(""""song_song"."id" IN (SELECT U0."song_id" FROM "favourite_song_favouritesong" U0 WHERE U0."author_id" = %s)""", params=[request.query_params.get('user')]))
            songs = songs.annotate(favourite=RawSQL("""(SELECT U0."id" FROM "favourite_song_favouritesong" U0 WHERE U0."song_id" = "song_song"."id" AND U0."author_id" = %s)""", params=[request.query_params.get('user')]))
        if 'offset' in request.query_params:
            offset = int(request.query_params.get('offset'))
        else:
            offset = 0
        print(songs.query)
        songs = songs[offset: offset + 20]

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
