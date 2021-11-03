from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from album_invitation.models import AlbumInvitation
from album_invitation.serializer import AlbumInvitationSerializer


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
