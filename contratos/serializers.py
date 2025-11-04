from rest_framework import serializers
from .models import *
from cableoperadores.serializers import *

class CajaEmpalmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja_empalme
        fields = '__all__'
        read_only_fields = ['contrato']
class CableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cable
        fields = '__all__'
        read_only_fields = ['contrato']
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['contrato']
class NapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nap
        fields = '__all__'
        read_only_fields = ['contrato']
class ContratoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    nap = NapSerializer(required=False)
    reserva = ReservaSerializer(required=False)
    caja_empalme = CajaEmpalmeSerializer(required=False)
    cable = CableSerializer(required=False)
    cableoperador = CableoperadoresSerializer(read_only=True)
    class Meta:
        model = Contratos
        fields = '__all__'
        read_only_fields = ['estado_display']
    def create(self, validated_data):
        # 1. Obtener los datos de 'nap' si existen en la petición
        nap_data = validated_data.pop('nap', None)
        cable_data = validated_data.pop('cable', None)
        caja_empalme_data = validated_data.pop('caja_empalme', None)
        reserva_data = validated_data.pop('reserva', None)
        
        # 2. Crear primero el objeto Contrato
        contrato = Contratos.objects.create(**validated_data)
        
        # 3. Si se enviaron datos de Nap, crea la Nap y asígnala al contrato
        if nap_data:
            nap_instance = Nap.objects.create(**nap_data)
            contrato.nap = nap_instance
        else:
            contrato.nap = Nap.objects.create(contrato=contrato)

        if cable_data:
            cable_instance = Cable.objects.create(**cable_data)
            contrato.cable = cable_instance
        else:
            contrato.cable = Cable.objects.create(contrato=contrato)

        if caja_empalme_data:
            caja_empalme_instance = Caja_empalme.objects.create(**caja_empalme_data)
            contrato.caja_empalme = caja_empalme_instance
        else:
            contrato.caja_empalme = Caja_empalme.objects.create(contrato=contrato)

        if reserva_data:
            reserva_instance = Reserva.objects.create(**reserva_data)
            contrato.reserva = reserva_instance
        else:
            contrato.reserva = Reserva.objects.create(contrato=contrato)

        contrato.save()
        return contrato

    ## 🛑 PASO 4: (Opcional) Implementar la lógica de actualización si es necesario
    def update(self, instance, validated_data):
        # 1. Extraer los datos de los modelos relacionados de validated_data
        # Usamos .pop() para removerlos y evitar que sean guardados como campos de Contrato
        nap_data = validated_data.pop('nap', None)
        cable_data = validated_data.pop('cable', None)
        caja_empalme_data = validated_data.pop('caja_empalme', None)
        reserva_data = validated_data.pop('reserva', None)
        
        # 2. Actualizar campos del modelo principal (Contratos)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 3. Actualizar los modelos relacionados si los datos fueron enviados
        
        # Actualizar la NAP asociada
        if nap_data and instance.nap:
            # Itera sobre los campos enviados y actualiza la instancia de nap
            for attr, value in nap_data.items():
                setattr(instance.nap, attr, value)
            instance.nap.save() # Guarda los cambios en el modelo Nap
        
        # Actualizar el CABLE asociado
        if cable_data and instance.cable:
            # Itera sobre los campos enviados y actualiza la instancia de cable
            for attr, value in cable_data.items():
                setattr(instance.cable, attr, value)
            instance.cable.save() # Guarda los cambios en el modelo Cable
            
        # Actualizar la CAJA_EMPALME asociada
        if caja_empalme_data and instance.caja_empalme:
            # Itera sobre los campos enviados y actualiza la instancia de caja_empalme
            for attr, value in caja_empalme_data.items():
                setattr(instance.caja_empalme, attr, value)
            instance.caja_empalme.save() # Guarda los cambios en el modelo CajaEmpalme
            
        # Actualizar la RESERVA asociada
        if reserva_data and instance.reserva:
            # Itera sobre los campos enviados y actualiza la instancia de reserva
            for attr, value in reserva_data.items():
                setattr(instance.reserva, attr, value)
            instance.reserva.save() # Guarda los cambios en el modelo Reserva
                
        return instance

    def validate(self, data):
        # Validar que la fecha de fin sea posterior a la fecha de inicio
        if data.get('fin_vigencia') and data.get('inicio_vigencia'):
            if data['fin_vigencia'] <= data['inicio_vigencia']:
                raise serializers.ValidationError({
                    "fin_vigencia": "La fecha de finalización debe ser posterior a la fecha de inicio"
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
    
    class Meta:
        model = Cableoperadores
        fields = '__all__'

    def get_contrato_vigente(self, obj):
        contrato = obj.contratos.filter(estado='VIGENTE').first()
        if contrato:
            return ContratoSerializer(contrato).data
        return None
