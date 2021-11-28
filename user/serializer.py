from django.contrib.auth import get_user_model
from song.models import Song
from rest_framework import serializers, permissions


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        if 'first_name' in validated_data:
            instance.first_name = validated_data.get('first_name')
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name')
        if 'email' in validated_data:
            instance.email = validated_data.get('email')
        instance.save()
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
