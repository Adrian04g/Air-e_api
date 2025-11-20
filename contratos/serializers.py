from rest_framework import serializers
from .models import *
from django.db import transaction
from cableoperadores.serializers import *
from cableoperadores.models import Cableoperadores


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
        #read_only_fields = ['contrato']


class ContratoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    nap = NapSerializer(required=False)
    reserva = ReservaSerializer(required=False)
    caja_empalme = CajaEmpalmeSerializer(required=False)
    cable = CableSerializer(required=False)
    # Representación completa en la respuesta
    cableoperador = CableoperadoresSerializer(read_only=True)
    # Permitir enviar solo el ID del cable-operador al crear/actualizar
    cableoperador_id = serializers.PrimaryKeyRelatedField(
        source='cableoperador',
        queryset=Cableoperadores.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Contratos
        fields = '__all__'
        read_only_fields = ['estado_display']

    def create(self, validated_data):
        nap_data = validated_data.pop('nap', None)
        cable_data = validated_data.pop('cable', None)
        caja_empalme_data = validated_data.pop('caja_empalme', None)
        reserva_data = validated_data.pop('reserva', None)

        # Crear todo dentro de una transacción para evitar estados incompletos
        with transaction.atomic():
            # Crear primero el objeto Contrato
            contrato = Contratos.objects.create(**validated_data)

            # Crear/ligar objetos OneToOne asegurando que siempre se asigne la FK 'contrato'
            if nap_data:
                nap_instance = Nap.objects.create(contrato=contrato, **nap_data)
                contrato.nap = nap_instance
            else:
                contrato.nap = Nap.objects.create(contrato=contrato)

            if cable_data:
                cable_instance = Cable.objects.create(contrato=contrato, **cable_data)
                contrato.cable = cable_instance
            else:
                contrato.cable = Cable.objects.create(contrato=contrato)

            if caja_empalme_data:
                caja_empalme_instance = Caja_empalme.objects.create(contrato=contrato, **caja_empalme_data)
                contrato.caja_empalme = caja_empalme_instance
            else:
                contrato.caja_empalme = Caja_empalme.objects.create(contrato=contrato)

            if reserva_data:
                reserva_instance = Reserva.objects.create(contrato=contrato, **reserva_data)
                contrato.reserva = reserva_instance
            else:
                contrato.reserva = Reserva.objects.create(contrato=contrato)

            contrato.save()

        return contrato

    def update(self, instance, validated_data):
        nap_data = validated_data.pop('nap', None)
        cable_data = validated_data.pop('cable', None)
        caja_empalme_data = validated_data.pop('caja_empalme', None)
        reserva_data = validated_data.pop('reserva', None)

        # Si se envió un nuevo cableoperador (viene como instancia por PrimaryKeyRelatedField), asignarlo
        # pero solo si no es None (evitar asignar NULL que violaría la restricción NOT NULL)
        if 'cableoperador' in validated_data:
            new_co = validated_data.pop('cableoperador')
            if new_co is not None:
                instance.cableoperador = new_co

        # Actualizar campos del modelo principal (Contratos)
        for attr, value in validated_data.items():
            # Evitar sobrescribir la relación cableoperador si viene como None
            if attr == 'cableoperador' and value is None:
                continue
            setattr(instance, attr, value)
        instance.save()

        # Actualizar/crear los modelos relacionados según los datos enviados

        # NAP
        if nap_data:
            if hasattr(instance, 'nap') and instance.nap:
                for attr, value in nap_data.items():
                    setattr(instance.nap, attr, value)
                instance.nap.save()
            else:
                # No existía, crearla ligada al contrato
                Nap.objects.create(contrato=instance, **nap_data)

        # CABLE
        if cable_data:
            if hasattr(instance, 'cable') and instance.cable:
                for attr, value in cable_data.items():
                    setattr(instance.cable, attr, value)
                instance.cable.save()
            else:
                Cable.objects.create(contrato=instance, **cable_data)

        # CAJA EMPALME
        if caja_empalme_data:
            if hasattr(instance, 'caja_empalme') and instance.caja_empalme:
                for attr, value in caja_empalme_data.items():
                    setattr(instance.caja_empalme, attr, value)
                instance.caja_empalme.save()
            else:
                Caja_empalme.objects.create(contrato=instance, **caja_empalme_data)

        # RESERVA
        if reserva_data:
            if hasattr(instance, 'reserva') and instance.reserva:
                for attr, value in reserva_data.items():
                    setattr(instance.reserva, attr, value)
                instance.reserva.save()
            else:
                Reserva.objects.create(contrato=instance, **reserva_data)

        return instance

    def validate(self, data):
        # Validar que la fecha de fin sea posterior a la fecha de inicio
        if data.get('fin_vigencia') and data.get('inicio_vigencia'):
            if data['fin_vigencia'] <= data['inicio_vigencia']:
                raise serializers.ValidationError({
                    "fin_vigencia": "La fecha de finalización debe ser posterior a la fecha de inicio"
                })
        # Validar que no exista otro contrato vigente para el mismo cableoperador
        # Usamos los nombres reales del modelo: 'cableoperador' y 'estado_contrato'
        if self.instance is None:  # Solo para crear nuevo contrato
            cableoperador = data.get('cableoperador')
            estado_val = data.get('estado_contrato')
            if cableoperador and estado_val and str(estado_val).lower().startswith('vig'):
                if Contratos.objects.filter(
                    cableoperador=cableoperador,
                    estado_contrato='Vigente'
                ).exists():
                    raise serializers.ValidationError(
                        "Ya existe un contrato vigente para este cableoperador"
                    )
        return data


class CableoperadorSerializer(serializers.ModelSerializer):
    cableoperador = CableoperadoresSerializer(read_only=True)
    class Meta:
        model = Cableoperadores
        fields = '__all__'

    def get_contrato_vigente(self, obj):
        # El related_name por defecto es 'contratos_set'
        contrato = Contratos.objects.filter(cableoperador=obj, estado_contrato='Vigente').first()
        if contrato:
            return ContratoSerializer(contrato).data
        return None
