from django.db.models import F, OuterRef
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from albums.serializer import AlbumSerializer, AlbumSongSerializer
from albums.models import Album, AlbumsSong
from rest_framework import permissions
from favourite_album.models import FavouriteAlbum


class AlbumList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        album = Album.objects.all()
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
            if request.query_params.get('favourite'):
                album = album.filter(favourite__isnull=False)

        if 'private' in request.query_params:
            if request.query_params.get('private') and 'user_id' in locals():
                album = album.filter(owners__in=[user_id])
                print(album.query)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            album = album.filter(public__exact=True)
        if 'get_all' not in request.query_params:
            album = album[offset: offset + 20]
        print(album.query)
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
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
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
