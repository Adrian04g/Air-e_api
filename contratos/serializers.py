from rest_framework import serializers
from .models import *

class ContratoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    #nap = serializers.PrimaryKeyRelatedField(queryset=Nap.objects.all())
    class Meta:
        model = Contratos
        fields = '__all__'
        read_only_fields = ['estado_display', 'nap']

    def validate(self, data):
        # Validar que la fecha de fin sea posterior a la fecha de inicio
        if data.get('fecha_fin') and data.get('fecha_inicio'):
            if data['fecha_fin'] <= data['fecha_inicio']:
                raise serializers.ValidationError({
                    "fecha_fin": "La fecha de finalización debe ser posterior a la fecha de inicio"
                })
        
        # Validar que no exista otro contrato vigente para el mismo cableoperador
        if self.instance is None:  # Solo para crear nuevo contrato
            cableoperador = data.get('cableoperador')
            if cableoperador and data.get('estado') == 'VIGENTE':
                if Contratos.objects.filter(
                    cableoperador=cableoperador,
                    estado='VIGENTE'
                ).exists():
                    raise serializers.ValidationError(
                        "Ya existe un contrato vigente para este cableoperador"
                    )
        return data

class CableoperadorSerializer(serializers.ModelSerializer):
    contratos = ContratoSerializer(many=True, read_only=True)
    contrato_vigente = serializers.SerializerMethodField()

    class Meta:
        model = Cableoperadores
        fields = '__all__'

    def get_contrato_vigente(self, obj):
        contrato = obj.contratos.filter(estado='VIGENTE').first()
        if contrato:
            return ContratoSerializer(contrato).data
        return None
