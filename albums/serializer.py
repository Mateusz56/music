from django.db.models import Avg
from rest_framework import serializers
from albums.models import Album, AlbumsSong
from song.serializer import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    songs_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    marks_avg = serializers.IntegerField(read_only=True)
    favourite = serializers.IntegerField(read_only=True, required=False)
    add_song = serializers.IntegerField(write_only=True, required=False)
    remove_song = serializers.IntegerField(write_only=True, required=False)
    add_owner = serializers.IntegerField(write_only=True, required=False)
    remove_owner = serializers.IntegerField(write_only=True, required=False)
    name = serializers.CharField(required=True, min_length=1)

    class Meta:
        model = Album
        fields = ['id', 'name', 'songs_count', 'comments_count', 'marks_avg', 'favourite', 'public', 'owners',
                  'add_song', 'remove_song', 'add_owner', 'remove_owner']

    def create(self, validated_data):
        album = Album(name=validated_data.get('name'), public=validated_data.get('public'))
        album.save()
        for owner in validated_data.get('owners'):
            album.owners.add(owner.id)
        album.save()
        return album

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if 'add_song' in validated_data:
            instance.songs.add(validated_data.get('add_song'))
        if 'owners' in validated_data:
            instance.owners.add(validated_data.get('owners'))
        instance.public = validated_data.get('public', instance.public)
        instance.save()
        return instance


class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumsSong
        fields = ['album', 'song', 'add_date']

    def create(self, validated_data):
        return AlbumsSong.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.songs = validated_data.get('songs', instance.songs)
        instance.owners = validated_data.get('owners', instance.owners)
        instance.save()
        return instance
