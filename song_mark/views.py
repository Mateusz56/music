import json

from django.db.models import F, Avg
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict

from music import Permissions
from song.models import Song
from song_mark.serializer import SongMarkSerializer
from song_mark.models import SongMark
from rest_framework import permissions
from django.contrib.auth import get_user_model


class SongMarkView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, Permissions.IsAuthorPermissionOrReadonly]

    def get(self, request, format=None):
        song_mark = SongMark.objects.all()
        if 'targetId' in request.query_params:
            song_mark = song_mark.filter(song_id=request.query_params.get('targetId'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        song_mark = song_mark.aggregate(avg=Avg('mark'))
        return Response(song_mark)

    def post(self, request, format=None):
        serializer = SongMarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongMarkDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, Permissions.IsAuthorPermissionOrReadonly]

    def get(self, request, format=None):
        try:
            if 'targetId' in request.query_params:
                song_mark = SongMark.objects.all()
                author = request.user
                song_mark = song_mark.filter(author=author)
                song_mark = song_mark.get(song=request.query_params.get('targetId'))
                return Response(model_to_dict(song_mark), status=status.HTTP_200_OK)
        except SongMark.DoesNotExist:
            return Response(data={}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        song_mark = SongMark.objects.all()
        body = json.loads(request.body)
        author_id = Token.objects.get(key=body['author']).user_id
        song_mark = song_mark.filter(author_id=author_id).filter(song_id=body['song'])
        if not song_mark:
            song_mark = SongMark(author_id=author_id, song_id=body['song'], mark=body['mark'])
            song_mark.save()
            return Response(model_to_dict(song_mark), status=status.HTTP_201_CREATED)
        else:
            song_mark.update(mark=body['mark'])
            return Response(model_to_dict(song_mark[0]), status=status.HTTP_200_OK)
