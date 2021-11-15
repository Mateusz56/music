import json

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from album_comment.models import AlbumComment
from album_invitation.models import AlbumInvitation
from album_invitation.serializer import AlbumInvitationSerializer
from album_mark.models import AlbumMark
from albums.models import AlbumsSong


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


class AlbumInvitationUser(View):
    permission_classes = [permissions.AllowAny]
    serializer_class = AlbumInvitationSerializer

    def get(self, request, *args, **kwargs):
        user = self.kwargs['user']
        response = HttpResponse(content_type='application/json')
        response.status_code = 200
        querySet = AlbumInvitation.objects.filter(user=user)
        querySet = querySet.select_related('album')
        values = querySet.values('album', 'album__name')
        ret = []
        response.write('{"albums": ')
        for v in values:
            ret.append({"album": v.get('album'), 'album_name': v.get('album__name'),
                        'comment_count': AlbumComment.objects.filter(album=v['album']).count(),
                        'song_count': AlbumsSong.objects.filter(album=v['album']).count(),
                        'mark_avg': AlbumMark.objects.filter(album=v['album']).aggregate(Avg('mark'))['mark__avg']})
        response.write(str(ret).replace("'", '"').replace('None', 'null'))
        response.write('}')
        return response

    def post(self, request, *args, **kwargs):
        print(self.kwargs)
        return 'asd'
