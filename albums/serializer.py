from rest_framework import serializers
from albums.models import Album, AlbumsSong


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'songs', 'owners']

    def create(self, validated_data):
        return Album.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.songs = validated_data.get('songs', instance.author)
        instance.owners = validated_data.get('owners', instance.create_date)
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
