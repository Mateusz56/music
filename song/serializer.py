from rest_framework import serializers
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['title', 'performer', 'year', 'genre']

    def create(self, validated_data):
        return Song.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.performer = validated_data.get('performer', instance.performer)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance
