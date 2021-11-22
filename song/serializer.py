from django.db.models import Avg
from rest_framework import serializers, permissions
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    marks_avg = serializers.FloatField(read_only=True)
    favourite = serializers.IntegerField(read_only=True)
    sort_mode = serializers.CharField(read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'performer', 'year', 'genre', 'comments_count', 'marks_avg', 'favourite', 'sort_mode']

    def create(self, validated_data):
        return Song.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.performer = validated_data.get('performer', instance.performer)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance
