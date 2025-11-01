from rest_framework import serializers
from .models import Cableoperadores
from django.contrib.auth.models import User, Group

class CableoperadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cableoperadores
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']