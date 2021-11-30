from django.db.models import F, OuterRef, Value, Avg, Count
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from album_comment.models import AlbumComment
from album_mark.models import AlbumMark
from albums.serializer import AlbumSerializer, AlbumSongSerializer
from albums.models import Album, AlbumsSong
from rest_framework import permissions
from favourite_album.models import FavouriteAlbum
from music import Permissions


class AlbumList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        album = Album.objects.all()

        marks_subquery = AlbumMark.objects.filter(album_id=OuterRef('id'))
        marks_subquery = marks_subquery.annotate(dummy=Value(1)).values('dummy').annotate(marks_avg=Avg('mark')).values_list('marks_avg')
        album = album.annotate(marks_avg=marks_subquery)

        comments_subquery = AlbumComment.objects.filter(album_id=OuterRef('id'))
        comments_subquery = comments_subquery.annotate(dummy=Value(1)).values('dummy').annotate(count=Count('*')).values_list('count')
        album = album.annotate(comments_count=comments_subquery)

        songs_count_subquery = AlbumsSong.objects.filter(album_id=OuterRef('id'))
        songs_count_subquery = songs_count_subquery.annotate(dummy=Value(1)).values('dummy').annotate(count=Count('*')).values_list('count')
        album = album.annotate(songs_count=songs_count_subquery)

        if 'page' in request.query_params:
            offset = 20 * int(request.query_params.get('page'))
        else:
            offset = 0

        if 'name' in request.query_params:
            album = album.filter(name__contains=request.query_params.get('name'))
        if 'user' in request.query_params:
            user_id = request.query_params.get('user')
            favourite_subquery = FavouriteAlbum.objects.filter(author_id=user_id, album_id=OuterRef('id')).values('id')
            album = album.annotate(favourite=favourite_subquery)

        if 'favourite' in request.query_params:
            if request.query_params.get('favourite') and request.query_params.get('favourite') != 'false':
                album = album.filter(favourite__isnull=False)

        if 'sortMode' in request.query_params:
            album = album.order_by(request.query_params.get('sortMode'))

        if 'private' in request.query_params and request.query_params.get('private') != 'false':
            if request.query_params.get('private') and 'user_id' in locals():
                album = album.filter(owners__in=[user_id])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            album = album.filter(public__exact=True)
        if 'get_all' not in request.query_params:
            album = album[offset: offset + 20]

        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetail(APIView):
    permission_classes = [Permissions.AlbumPermission]

    def get_object(self, pk):
        try:
            album = Album.objects.get(pk=pk)
            self.check_object_permissions(self.request, album)
            return album
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
