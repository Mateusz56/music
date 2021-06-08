from rest_framework import serializers
from album_mark.models import AlbumMark


class SongMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumMark
        fields = '__all__'

    def create(self, validated_data):
        return AlbumMark.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.author = validated_data.get('author', instance.author)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.mark = validated_data.get('mark', instance.content)
        instance.save()
        return instance
