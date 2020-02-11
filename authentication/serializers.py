from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from authentication.models import User
from authentication.constants import *


class TokenMixin:
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


class UserSerializer(serializers.ModelSerializer, TokenMixin):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'image']


class UserWithTokenSerializer(serializers.ModelSerializer, TokenMixin):
    token = serializers.SerializerMethodField() # manually create token
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['token', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        new_user = self.Meta.model(**validated_data)
        if password is not None:
            new_user.set_password(password)
        new_user.save()
        return new_user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
