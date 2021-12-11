from rest_framework import serializers
from rest_framework.fields import CharField

from album_comment.models import AlbumComment


class AlbumCommentSerializer(serializers.ModelSerializer):
    content = CharField(required=True, min_length=3)

    class Meta:
        model = AlbumComment
        fields = ['id', 'album', 'author', 'create_date', 'content']

    def create(self, validated_data):
        return AlbumComment.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.author = validated_data.get('author', instance.author)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
