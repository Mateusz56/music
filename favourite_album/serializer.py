from rest_framework import serializers
from favourite_album.models import FavouriteAlbum


class FavouriteAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteAlbum
        fields = '__all__'

    def create(self, validated_data):
        return FavouriteAlbum.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance
