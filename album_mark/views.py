from django.db.models import Avg
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from album_mark.models import AlbumMark
from album_mark.serializer import AlbumMarkSerializer
from rest_framework import permissions
from music import Permissions


class AlbumMarkView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, Permissions.IsAuthorPermissionOrReadonly]
    authentication_classes = [TokenAuthentication]

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
            self.check_object_permissions(self.request, serializer.validated_data['album'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumMarkDetail(APIView):
    permission_classes = [Permissions.IsAuthorPermissionOrReadonly]

    def get(self, request, format=None):
        try:
            if 'targetId' in request.query_params:
                album_mark = AlbumMark.objects.all()
                author = request.user
                album_mark = album_mark.filter(author=author)
                album_mark = album_mark.get(album=request.query_params.get('targetId'))
                return Response(model_to_dict(album_mark), status=status.HTTP_200_OK)
        except AlbumMark.DoesNotExist:
            return Response(data={}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        album_mark = AlbumMark.objects.all()
        author_id = Token.objects.get(key=request.data['author']).user_id
        album_mark = album_mark.filter(author_id=author_id).filter(album_id=request.data['song']).first()

        if not album_mark:
            album_mark = AlbumMark(author_id=author_id, album_id=request.data['album'], mark=request.data['mark'])
            self.check_object_permissions(self.request, album_mark)
            album_mark.save()
            return Response(model_to_dict(album_mark), status=status.HTTP_201_CREATED)
        else:
            self.check_object_permissions(self.request, album_mark)
            album_mark.mark = request.data['mark']
            album_mark.save()
            return Response(model_to_dict(album_mark), status=status.HTTP_200_OK)
