import json
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from album_invitation.models import AlbumInvitation
from album_invitation.serializer import AlbumInvitationSerializer
from albums.models import Album
from django.http import HttpResponse

class FavouriteAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = AlbumInvitation.objects.all()
    serializer_class = AlbumInvitationSerializer


class FavouriteAlbumList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = AlbumInvitation.objects.all()
    serializer_class = AlbumInvitationSerializer

    def post(self, request, format=None, **kwargs):
        serializer = AlbumInvitationSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response(data=exc.args[0]['error'], status=exc.args[0]['status'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumInvitationUser(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AlbumInvitationSerializer

    lookup_field = 'userId'

    def get_queryset(self):
        queryset = AlbumInvitation.objects.filter(user=self.kwargs['userId'])
        return queryset

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        album_invitation = AlbumInvitation.objects.get(id=body['albumInvitation'])
        if body['accept'] == 1:
            album = album_invitation.album
            album.owners.add(album_invitation.user)
            album.save()

        album_invitation.delete()
        return HttpResponse(status=200)
