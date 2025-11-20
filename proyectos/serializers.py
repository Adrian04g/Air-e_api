from rest_framework import serializers
from .models import *
from django.db import transaction
from cableoperadores.serializers import CableoperadoresSerializer
from cableoperadores.models import Cableoperadores


class CajaEmpalmeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Caja_empalme
		fields = '__all__'
		read_only_fields = ['proyecto']


class CableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cable
		fields = '__all__'
		read_only_fields = ['proyecto']


class ReservaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reserva
		fields = '__all__'
		read_only_fields = ['proyecto']


class NapSerializer(serializers.ModelSerializer):
	class Meta:
		model = Nap
		fields = '__all__'
		read_only_fields = ['proyecto']


class AlturaInicialPosteSerializer(serializers.ModelSerializer):
	class Meta:
		model = AlturaInicialPoste
		fields = ['tipo8','tipo9','tipo10','tipo11','tipo12','tipo14','tipo16']


class IngresoProyectoSerializer(serializers.ModelSerializer):
	# Representación completa de cableoperador y permitir enviar solo el id
	cableoperador = CableoperadoresSerializer(read_only=True)
	cableoperador_id = serializers.PrimaryKeyRelatedField(
		source='cableoperador',
		queryset=Cableoperadores.objects.all(),
		write_only=True,
		required=False,
		allow_null=True,
	)
	# Altura inicial del poste (lectura mediante método, escritura directa)
	altura_inicial_poste = serializers.SerializerMethodField()
	# Campo de escritura para altura_inicial_poste
	altura_inicial_poste_input = AlturaInicialPosteSerializer(write_only=True, required=False, allow_null=True, source='altura_inicial_poste')
    
	class Meta:
		model = IngresoProyecto
		fields = ['cableoperador', 'cableoperador_id', 'OT_PRST', 'nombre', 'rechazado_GD', 
		          'cancelado', 'incluir_contrato', 'negado', 'TipoIngreso', 'departamento',
		          'municipio', 'barrio', 'fecha_inicio', 'fecha_fin', 'fecha_confirmacion_fin',
		          'fecha_radicacion_prst', 'fecha_revision_doc', 'fecha_entrega_coordinador',
		          'estado_ingreso', 'observaciones', 'altura_inicial_poste', 'altura_inicial_poste_input']

	def get_altura_inicial_poste(self, obj):
		"""Lectura: retorna objeto con datos o crea si no existe"""
		try:
			alp = obj.altura_inicial_poste
			if alp:
				return {
					'tipo8': alp.tipo8,
					'tipo9': alp.tipo9,
					'tipo10': alp.tipo10,
					'tipo11': alp.tipo11,
					'tipo12': alp.tipo12,
					'tipo14': alp.tipo14,
					'tipo16': alp.tipo16,
				}
		except AlturaInicialPoste.DoesNotExist:
			pass
		
		# Si no existe, crear uno por defecto y retornarlo
		alp, created = AlturaInicialPoste.objects.get_or_create(proyecto=obj)
		return {
			'tipo8': alp.tipo8,
			'tipo9': alp.tipo9,
			'tipo10': alp.tipo10,
			'tipo11': alp.tipo11,
			'tipo12': alp.tipo12,
			'tipo14': alp.tipo14,
			'tipo16': alp.tipo16,
		}

	def create(self, validated_data):
		altura_data = validated_data.pop('altura_inicial_poste', None)
		with transaction.atomic():
			ingreso = IngresoProyecto.objects.create(**validated_data)
			# Usar get_or_create para evitar IntegrityError si ya existe
			if altura_data:
				AlturaInicialPoste.objects.get_or_create(
					proyecto=ingreso,
					defaults=altura_data
				)
			else:
				# Crear registro por defecto si no se envían datos
				AlturaInicialPoste.objects.get_or_create(proyecto=ingreso)
		return ingreso

	def update(self, instance, validated_data):
		altura_data = validated_data.pop('altura_inicial_poste', None)

		# Actualizar campos del IngresoProyecto
		# Solo actualizar si el campo viene en validated_data (evita sobrescribir con None)
		for attr, value in validated_data.items():
			# Nunca sobrescribir cableoperador si no se envía (solo actualizar si viene)
			if attr == 'cableoperador' and value is None:
				continue
			setattr(instance, attr, value)
		instance.save()

		# Actualizar/crear AlturaInicialPoste
		if altura_data is not None:
			# get_or_create es seguro: obtiene o crea
			alp, created = AlturaInicialPoste.objects.get_or_create(proyecto=instance)
			# Actualizar campos si se enviaron datos
			for k, v in altura_data.items():
				setattr(alp, k, v)
			alp.save()

		return instance


class ProyectosSerializer(serializers.ModelSerializer):
	datos_ingreso = IngresoProyectoSerializer(read_only=True)
	datos_ingreso_id = serializers.PrimaryKeyRelatedField(
		source='datos_ingreso',
		queryset=IngresoProyecto.objects.all(),
		write_only=True,
	)

	# Related OneToOne objects (opcionales en la entrada)
	cable = CableSerializer(required=False)
	caja_empalme = CajaEmpalmeSerializer(required=False)
	reserva = ReservaSerializer(required=False)
	nap = NapSerializer(required=False)

	class Meta:
		model = Proyectos
		fields = '__all__'

	def create(self, validated_data):
		cable_data = validated_data.pop('cable', None)
		caja_data = validated_data.pop('caja_empalme', None)
		reserva_data = validated_data.pop('reserva', None)
		nap_data = validated_data.pop('nap', None)

		with transaction.atomic():
			proyecto = Proyectos.objects.create(**validated_data)

			# Crear/asegurar OneToOne relacionados
			if cable_data:
				Cable.objects.create(proyecto=proyecto, **cable_data)
			else:
				Cable.objects.create(proyecto=proyecto)

			if caja_data:
				Caja_empalme.objects.create(proyecto=proyecto, **caja_data)
			else:
				Caja_empalme.objects.create(proyecto=proyecto)

			if reserva_data:
				Reserva.objects.create(proyecto=proyecto, **reserva_data)
			else:
				Reserva.objects.create(proyecto=proyecto)

			if nap_data:
				Nap.objects.create(proyecto=proyecto, **nap_data)
			else:
				Nap.objects.create(proyecto=proyecto)

		return proyecto

	def update(self, instance, validated_data):
		cable_data = validated_data.pop('cable', None)
		caja_data = validated_data.pop('caja_empalme', None)
		reserva_data = validated_data.pop('reserva', None)
		nap_data = validated_data.pop('nap', None)

		# Actualizar FK datos_ingreso si se envió
		if 'datos_ingreso' in validated_data:
			new_di = validated_data.pop('datos_ingreso')
			if new_di is not None:
				instance.datos_ingreso = new_di

		# Actualizar campos directos del modelo Proyectos
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()

		# Actualizar/crear relacionados
		if cable_data:
			try:
				cable_inst = instance.cable
				for attr, value in cable_data.items():
					setattr(cable_inst, attr, value)
				cable_inst.save()
			except Cable.DoesNotExist:
				Cable.objects.create(proyecto=instance, **cable_data)

		if caja_data:
			try:
				caja_inst = instance.caja_empalme
				for attr, value in caja_data.items():
					setattr(caja_inst, attr, value)
				caja_inst.save()
			except Caja_empalme.DoesNotExist:
				Caja_empalme.objects.create(proyecto=instance, **caja_data)

		if reserva_data:
			try:
				reserva_inst = instance.reserva
				for attr, value in reserva_data.items():
					setattr(reserva_inst, attr, value)
				reserva_inst.save()
			except Reserva.DoesNotExist:
				Reserva.objects.create(proyecto=instance, **reserva_data)

		if nap_data:
			try:
				nap_inst = instance.nap
				for attr, value in nap_data.items():
					setattr(nap_inst, attr, value)
				nap_inst.save()
			except Nap.DoesNotExist:
				Nap.objects.create(proyecto=instance, **nap_data)

		return instance

	def validate(self, data):
		# Ejemplo: validar que la fecha de análisis no sea anterior a la inspección
		fecha_inspeccion = data.get('fecha_inspeccion')
		fecha_analisis = data.get('fecha_analisis_inspeccion')
		if fecha_inspeccion and fecha_analisis:
			if fecha_analisis < fecha_inspeccion:
				raise serializers.ValidationError({
					'fecha_analisis_inspeccion': 'La fecha de análisis no puede ser anterior a la fecha de inspección.'
				})
		return data


