from dataclasses import fields
from rest_framework import serializers
from api import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'firstname', 'email', 'lat', 'lon', 'location', 'token']
        depth = 1


    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class LocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=22, decimal_places=16)
    long = serializers.DecimalField(max_digits=22, decimal_places=16)
    