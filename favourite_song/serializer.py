from rest_framework import serializers
from favourite_song.models import FavouriteSong


class FavouriteSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteSong
        fields = ['id', 'song']

    author = serializers.CurrentUserDefault()

    def create(self, validated_data):
        return FavouriteSong.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.song = validated_data.get('song', instance.song)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance
