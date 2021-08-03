import json

from django.db.models import F, Avg
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict

from album_mark.models import AlbumMark
from album_mark.serializer import AlbumMarkSerializer
from song_mark.models import SongMark
from rest_framework import permissions


class AlbumMarkView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        album_mark = AlbumMark.objects.all()
        if 'targetId' in request.query_params:
            album_mark = album_mark.filter(album_id=request.query_params.get('targetId'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        album_mark = album_mark.aggregate(avg=Avg('mark'))
        return Response(album_mark)

    def post(self, request, format=None):
        serializer = AlbumMarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumMarkDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        try:
            if 'token' in request.query_params and 'targetId' in request.query_params:
                album_mark = AlbumMark.objects.all()
                author = Token.objects.get(key=request.query_params.get('token'))
                album_mark = album_mark.filter(author=author.user_id)
                album_mark = album_mark.get(album=request.query_params.get('targetId'))
                return Response(model_to_dict(album_mark), status=status.HTTP_200_OK)
        except AlbumMark.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print(request.body)
        album_mark = AlbumMark.objects.all()
        body = json.loads(request.body)
        author_id = Token.objects.get(key=body['author']).user_id
        album_mark = album_mark.filter(author_id=author_id).filter(album_id=body['song'])
        if not album_mark:
            album_mark = AlbumMark(author_id=author_id, album_id=body['album'], mark=body['mark'])
            album_mark.save()
            return Response(model_to_dict(album_mark), status=status.HTTP_201_CREATED)
        else:
            album_mark.update(mark=body['mark'])
            return Response(model_to_dict(album_mark[0]), status=status.HTTP_200_OK)
