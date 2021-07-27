from django.db.models import Avg
from rest_framework import serializers
from albums.models import Album, AlbumsSong
from song.serializer import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    songs_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    marks_avg = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'songs_count', 'comments_count', 'marks_avg']

    def get_songs_count(self, obj):
        return obj.songs.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_marks_avg(self, obj):
        return obj.album_marks.aggregate(Avg('mark'))['mark__avg']

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
