from rest_framework import serializers
from album_comment.models import AlbumComment


class AlbumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumComment
        fields = ['album', 'author', 'create_date', 'content']

    def create(self, validated_data):
        return AlbumComment.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.author = validated_data.get('author', instance.author)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
