from rest_framework import serializers
from song_mark.models import SongMark


class SongMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongMark
        fields = '__all__'

    def create(self, validated_data):
        return SongMark.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.song = validated_data.get('song', instance.song)
        instance.author = validated_data.get('author', instance.author)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.mark = validated_data.get('mark', instance.content)
        instance.save()
        return instance
