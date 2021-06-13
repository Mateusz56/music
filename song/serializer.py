from django.db.models import Avg
from rest_framework import serializers, permissions
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    song_marks = serializers.StringRelatedField(many=True)
    marks_avg = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Song
        fields = ['title', 'performer', 'year', 'genre', 'comments_count', 'comments', 'song_marks', 'marks_avg']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_marks_avg(self, obj):
        return obj.song_marks.aggregate(Avg('mark'))['mark__avg']

    def create(self, validated_data):
        return Song.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.performer = validated_data.get('performer', instance.performer)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance
