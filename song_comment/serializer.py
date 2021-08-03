from rest_framework import serializers
from song_comment.models import SongComment


class SongCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongComment
        fields = ['id', 'song', 'author', 'create_date', 'content']

    def create(self, validated_data):
        return SongComment.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.song = validated_data.get('song', instance.song)
        instance.author = validated_data.get('author', instance.author)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
