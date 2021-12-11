from django.db.models import F
from django.forms import model_to_dict
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from song_comment.serializer import SongCommentSerializer
from song_comment.models import SongComment
from rest_framework import permissions
import json


class SongCommentList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        song_comment = SongComment.objects.all()
        if 'targetId' in request.query_params:
            song_comment = SongComment.objects.filter(song=request.query_params.get('targetId'))
        if 'offset' in request.query_params:
            offset = int(request.query_params.get('offset'))
        else:
            offset = 0
        song_comment = song_comment.select_related('author').annotate(username=F('author__username'))
        song_comment = song_comment[offset * 20: offset * 20 + 20]
        return Response(song_comment.values())

    def post(self, request, format=None):
        body = json.loads(request.body)
        author = Token.objects.get(key=body['token']).user_id
        if len(body['content']) < 3:
            return Response(data={'content': ['Komentarz musi zawierać co najmniej 3 znaki.']},
                            status=status.HTTP_400_BAD_REQUEST)
        song_comment = SongComment(author_id=author, song_id=body['song'], content=body['content'])
        song_comment.save()
        return Response(model_to_dict(song_comment), status=status.HTTP_201_CREATED)


class SongCommentDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return SongComment.objects.get(pk=pk)
        except SongComment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        song_comment = self.get_object(pk)
        serializer = SongCommentSerializer(song_comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        song_comment = self.get_object(pk)
        serializer = SongCommentSerializer(song_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        song_comment = self.get_object(pk)
        song_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
