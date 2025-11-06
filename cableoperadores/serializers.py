from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
class CableoperadoresSerializer(serializers.ModelSerializer):
    ejecutiva = UserSerializer(read_only=True)
    ejecutiva_id = serializers.PrimaryKeyRelatedField(
        source='ejecutiva',
        queryset=User.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Cableoperadores
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        
class NotificacionSerializer(serializers.ModelSerializer):
    cableoperador = CableoperadoresSerializer(read_only=True)
    cableoperador_id = serializers.PrimaryKeyRelatedField(queryset=Cableoperadores.objects.all(), write_only=True, source='cableoperador')
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo_notificacion', 'fecha', 'cableoperador', 'cableoperador_id']