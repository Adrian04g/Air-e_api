from rest_framework import serializers
from .models import Cableoperadores
from django.contrib.auth.models import User, Group

Rliquidacion = [
    ('Calendarios', 'Calendarios'),
    ('Habiles', 'Habiles'),
]
ESTADOS_CONTRATO = [
    ('Contratado' , 'Contratado'),
    ('Finalizado' , 'Finalizado'),
    ('En_Renovacion' , 'En Renovacion'),
    ('Renovacion_firma_prst' , 'En Renovacion - Firma PRST'),
    ('Renovacion_firma_air_e' , 'En Renovacion - Firma AIR-E'),
    ('nuevo_firma_prst' , 'Nuevo - Firma PRST'),
    ('nuevo_firma_air_e' , 'Nuevo - Firma AIR-E'),
    ('En_Gestion' , 'En Gestion'),
    ('Sin_usos' , 'Sin Usos'),
]
class CableoperadoresSerializer1(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    nombre = serializers.CharField(max_length=100, required=True, allow_null=True)
    nombre_largo = serializers.CharField(max_length=255, required=False, allow_null=True)
    NIT = serializers.IntegerField(required=False, allow_null=True)
    Digito_verificacion = serializers.IntegerField(required=False, allow_null=True)
    RegistroTic = serializers.IntegerField(required=False, allow_null=True)
    CodigoInterno = serializers.IntegerField(required=False, allow_null=True)
    pais = serializers.CharField(max_length=100, required=False, allow_null=True)
    ciudad = serializers.CharField(max_length=100, required=False, allow_null=True)
    direccion = serializers.CharField(max_length=255, required=False, allow_null=True)
    Representante = serializers.CharField(max_length=100, required=False, allow_null=True)
    telefono = serializers.IntegerField(required=True,allow_null=True)
    correo = serializers.EmailField(max_length=100, required=True, allow_null=True)
    ejecutiva = serializers.CharField(max_length=100, required=False, allow_null=True)
    observaciones = serializers.CharField(max_length=1000, required=True, allow_null=True)
    estado = serializers.ChoiceField(choices=ESTADOS_CONTRATO, required=True, allow_null=True)
    vencimiento_factura = serializers.IntegerField(required=False, allow_null=True)
    preliquidacion_num = serializers.IntegerField(required=False, allow_null=True)
    preliquidacion_letra = serializers.CharField(max_length=100, required=False, allow_null=True)
    respuesta_preliquidacion = serializers.ChoiceField(choices=Rliquidacion, required=False, allow_null=True)

    
      

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