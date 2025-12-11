from rest_framework import serializers
from .models import *
from cableoperadores.serializers import CableoperadoresSerializer
from django.db.models import Sum

class RegistroPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = registro_pago
        fields = '__all__'
from decimal import Decimal
class FacturaSerializer(serializers.ModelSerializer):
    # Campo que calcula la suma de pagos (solo lectura)
    monto_pagado = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    #cableoperador = serializers.CharField(source='contratos.cableoperador.nombre', read_only=True)
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
    # Mostrar todos los registros de pago anidados
    pagos = RegistroPagoSerializer(many=True, read_only=True) 
    monto_pendiente = serializers.SerializerMethodField()
    class Meta:
        model = Facturacion
        fields = '__all__'

    def get_monto_pagado(self, obj):
        total = obj.pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or Decimal('0.00')
        # Asegurar Decimal si viene como float
        if isinstance(total, float):
            total = Decimal(str(total))
        return float(round(total, 2))

    def get_monto_pendiente(self, obj):
        total_pagos = obj.pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or Decimal('0.00')
        if isinstance(total_pagos, float):
            total_pagos = Decimal(str(total_pagos))
        # Convertir el valor facturado (float) a Decimal para la operación
        valor_facturado = obj.Valor_facturado_iva
        valor_facturado_dec = Decimal(str(valor_facturado)) if valor_facturado is not None else Decimal('0.00')
        pendiente = valor_facturado_dec - total_pagos
        return float(round(pendiente, 2))
    def get_estado(self, obj):
        monto_pagado = self.get_monto_pagado(obj)
        valor_facturado = obj.Valor_facturado_iva

        if monto_pagado == 0:
            return 'Pendiente'
        elif 0 < monto_pagado < valor_facturado:
            return 'PagadaParcial'
        elif monto_pagado >= valor_facturado:
            return 'Pagada'
        else:
            return obj.estado  # Retorna el estado original si no coincide con ninguna condición