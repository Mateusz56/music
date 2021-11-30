from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from album_invitation.models import AlbumInvitation
from album_invitation.serializer import AlbumInvitationSerializer
from django.http import HttpResponse, Http404

from music import Permissions


class FavouriteAlbumList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, Permissions.AlbumInvitationAuth]
    authentication_classes = [TokenAuthentication]
    queryset = AlbumInvitation.objects.all()
    serializer_class = AlbumInvitationSerializer

    def post(self, request, format=None, **kwargs):
        serializer = AlbumInvitationSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                self.check_object_permissions(self.request, serializer.validated_data['album'])
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response(data=exc.args[0]['error'], status=exc.args[0]['status'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumInvitationUser(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, Permissions.AlbumInvitationAuth]
    authentication_classes = [TokenAuthentication]
    serializer_class = AlbumInvitationSerializer
    lookup_field = 'userId'

    def get_object(self, pk):
        try:
            obj = AlbumInvitation.objects.get(pk=pk)
            return obj
        except AlbumInvitation.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queryset = AlbumInvitation.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        album_invitation = self.get_object(request.data.get('albumInvitation'))
        self.check_object_permissions(self.request, album_invitation)
        if request.data.get('accept') == 1:
            album = album_invitation.album
            album.owners.add(album_invitation.user)
            album.save()

        album_invitation.delete()
        return HttpResponse(status=200)
