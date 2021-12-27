from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Pole może zawierać tylko cyfry i litery.')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, required=False, write_only=True)
    first_name = serializers.CharField(min_length=2, required=True, validators=[alphanumeric])
    last_name = serializers.CharField(min_length=2, required=True, validators=[alphanumeric])
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

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


class CreateUserSerializer(UserSerializer):
    username = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=5, write_only=True)
    first_name = serializers.CharField(min_length=2, required=True, validators=[alphanumeric])
    last_name = serializers.CharField(min_length=2, required=True, validators=[alphanumeric])


class UpdateUserSerializer(UserSerializer):
    username = serializers.CharField(required=False, read_only=True)
    password = serializers.CharField(min_length=5, write_only=True, required=False)
    first_name = serializers.CharField(min_length=2, required=False, validators=[alphanumeric])
    last_name = serializers.CharField(min_length=2, required=False, validators=[alphanumeric])
    email = serializers.EmailField(required=False)
