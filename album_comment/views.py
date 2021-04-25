from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from album_comment.serializer import AlbumCommentSerializer
from album_comment.models import AlbumComment
from rest_framework import permissions


class AlbumCommentList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        album_comments = AlbumComment.objects.all()
        serializer = AlbumCommentSerializer(album_comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
