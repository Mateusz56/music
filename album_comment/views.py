from django.db.models import F
from django.forms import model_to_dict
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from album_comment.serializer import AlbumCommentSerializer
from album_comment.models import AlbumComment
from rest_framework import permissions
import json


class AlbumCommentList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

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
        print(request.headers['Accept-Language'])
        body = json.loads(request.body)
        author = request.user.id
        if len(body['content']) < 3:
            if 'Accept-Language' in request.headers:
                error_code = ['Komentarz musi zawierać co najmniej 3 znaki.' if request.headers['Accept-Language'].split(',')[0] == 'pl' else 'Comment must be at least 3 characters long.']
            else:
                error_code = 'Comment must be at least 3 characters long.'

            return Response(data={'content': [error_code]},
                            status=status.HTTP_400_BAD_REQUEST)
        album_comment = AlbumComment(author_id=author, album_id=body['album'], content=body['content'])
        album_comment.save()
        return Response(model_to_dict(album_comment), status=status.HTTP_201_CREATED)