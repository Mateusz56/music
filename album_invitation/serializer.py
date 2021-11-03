from django.contrib.auth.models import User
from requests import Response
from rest_framework import serializers, status
from album_invitation.models import AlbumInvitation
from albums.models import Album


class AlbumInvitationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AlbumInvitation
        fields = ['album', 'username']

    def is_valid(self, raise_exception=False):
        data = self._kwargs['data']
        user = User.objects.filter(username=data['username']).first()

        if user is None:
            raise serializers.ValidationError({'status': status.HTTP_404_NOT_FOUND, 'error': 'Użytkownik z podaną nazwą nie istnieje.'})
        album_invitation = AlbumInvitation.objects.filter(user=user).filter(album=data['album']).first()

        if album_invitation is not None:
            raise serializers.ValidationError({'status': status.HTTP_406_NOT_ACCEPTABLE, 'error': 'Podany użytkownik otrzymał już zaproszenie do tego albumu.'})
        album = Album.objects.filter(owners=user).first()

        if album is not None:
            raise serializers.ValidationError({'status': status.HTTP_406_NOT_ACCEPTABLE, 'error': 'Użytkownik jest już współwłaścicielem tego albumu.'})

        return super(AlbumInvitationSerializer, self).is_valid()

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data['username']).first()
        return AlbumInvitation.objects.create(user=user, album=validated_data['album'])

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
