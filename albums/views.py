from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from albums.serializer import AlbumSerializer, AlbumSongSerializer
from albums.models import Album, AlbumsSong
from rest_framework import permissions


class AlbumList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        album = Album.objects.all()
        if 'page' in request.query_params:
            offset = 20 * int(request.query_params.get('page'))
        else:
            offset = 0

        if 'name' in request.query_params:
            album = Album.objects.filter(name__contains=request.query_params.get('name'))

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
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
