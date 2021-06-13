from django.db.models import F
from django.forms import model_to_dict
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from album_comment.serializer import AlbumCommentSerializer
from album_comment.models import AlbumComment
from rest_framework import permissions
from rest_framework.authtoken.models import Token
import json


class AlbumCommentList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        album_comment = AlbumComment.objects.all()
        if 'targetId' in request.query_params:
            album_comment = AlbumComment.objects.filter(album=request.query_params.get('targetId'))
        if 'offset' in request.query_params:
            offset = int(request.query_params.get('offset'))
        else:
            offset = 0
        album_comment = album_comment.select_related('author').annotate(username=F('author__username'))
        album_comment = album_comment[offset * 20: offset * 20 + 20]
        return Response(album_comment.values())

    def post(self, request, format=None):
        body = json.loads(request.body)
        author = Token.objects.get(key=body['token']).user_id
        album_comment = AlbumComment(author_id=author, album_id=body['album'], content=body['content'])
        album_comment.save()
        return Response(model_to_dict(album_comment), status=status.HTTP_201_CREATED)


class AlbumCommentDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return AlbumComment.objects.get(pk=pk)
        except AlbumComment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album_comment = self.get_object(pk)
        serializer = AlbumCommentSerializer(album_comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        album_comment = self.get_object(pk)
        serializer = AlbumCommentSerializer(album_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album_comment = self.get_object(pk)
        album_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
