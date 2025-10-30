from rest_framework import serializers
from cableoperadores.serializers import CableoperadoresSerializerS
CLASIFICACION = [
    ('tipo1' , 'tipo1'),
    ('tipo2' , 'tipo2'),
    ('tipo3' , 'tipo3'),
]
ESTADOS_CONTRATO = [
    ('Vigente' , 'Vigente'),
    ('Vencido' , 'Vencido'),
]
TIPO_FECHA_RADICACION_CONTRATO = [
    ('fija' , 'Fija'),
    ('dinamica' , 'Dinámica'),
]
GARANTIA_CHOICES = [
    ('poliza_rce', 'Póliza de RCE'),
    ('poliza_cumplimiento', 'Póliza de Cumplimiento'),
]
VIGENCIA_AMPARO_CHOICES = [
    ('Igual_a_Duracion_de_Contrato_mas_12_Meses' , 'Igual a Duración de Contrato + 12 Meses'),
    ('Igual_a_Duracion_de_Contrato_mas_6_Meses' , 'Igual a Duración de Contrato + 6 Meses'),
    ('Igual_a_Duracion_de_Contrato_mas_4_Meses' , 'Igual a Duración de Contrato + 4 Meses'),
    ('Igual_a_Duracion_de_Contrato_mas_2_Meses' , 'Igual a Duración de Contrato + 2 Meses'),
]
MONTO_ASEGURADO_POLIZA_CUMPLIMIENTO_CHOICES = [
    ('15%_valor_contrato', '15% Valor del Contrato'),
    ('20%_valor_contrato', '20% Valor del Contrato'),
    ('30%_valor_contrato', '30% Valor del Contrato'),
    ('20%_valor_base_constitucion_poliza', '20% Valor base de Constitución de Póliza'),
    ('30%_valor_base_constitucion_poliza', '30% Valor base de Constitución de Póliza'),
]
MONTO_ASEGURADO_POLIZA_RCE_CHOICES = [
    ('no_inferior_100_SMLMV', 'No inferior a 100 SMLMV'),
    ('no_inferior_200_SMLMV', 'No inferior a 200 SMLMV'),
    ('no_inferior_300_SMLMV', 'No inferior a 300 SMLMV'),
]
class ContratoSerializerS(serializers.Serializer):
    cableoperador = serializers.IntegerField(allow_null=True)
    
    estado_contrato = serializers.ChoiceField(choices=ESTADOS_CONTRATO, allow_null=True)
    duracion_anos = serializers.IntegerField(default=0, allow_null=True)
    inicio_vigencia = serializers.DateField(allow_null=True)
    fin_vigencia = serializers.DateField(allow_null=True)
    valor_contrato = serializers.DecimalField(max_digits=20, decimal_places=2, default=0, allow_null=True)
    # Campos para la Póliza de Cumplimiento
    numero_poliza_cumplimiento = serializers.CharField(max_length=100, allow_null=True)
    vigencia_amparo_poliza_cumplimiento = serializers.ChoiceField(choices=VIGENCIA_AMPARO_CHOICES, allow_null=True)
    inicio_vigencia_poliza_cumplimiento = serializers.DateField(allow_null=True)
    fin_vigencia_poliza_cumplimiento = serializers.DateField(allow_null=True)
    monto_asegurado_poliza_cumplimiento = serializers.ChoiceField(choices=MONTO_ASEGURADO_POLIZA_CUMPLIMIENTO_CHOICES, allow_null=True)
    valor_monto_asegurado_poliza_cumplimiento = serializers.DecimalField(max_digits=20, decimal_places=2, allow_null=True)
    valor_asegurado_poliza_cumplimiento = serializers.CharField(max_length=100, allow_null=True)
    inicio_amparo_poliza_cumplimiento = serializers.DateField(allow_null=True)
    fin_amparo_poliza_cumplimiento = serializers.DateField(allow_null=True)
    expedicion_poliza_cumplimiento = serializers.DateField(allow_null=True)
    # Campos para la Póliza de RCE
    numero_poliza_rce = serializers.CharField(max_length=100, allow_null=True)
    vigencia_amparo_poliza_rce = serializers.ChoiceField(choices=VIGENCIA_AMPARO_CHOICES, allow_null=True)
    inicio_vigencia_poliza_rce = serializers.DateField(allow_null=True)
    fin_vigencia_poliza_rce = serializers.DateField(allow_null=True)
    monto_asegurado_poliza_rce = serializers.ChoiceField(choices=MONTO_ASEGURADO_POLIZA_RCE_CHOICES, allow_null=True)
    valor_monto_asegurado_poliza_rce = serializers.DecimalField(max_digits=20, decimal_places=2, allow_null=True)
    valor_asegurado_poliza_rce = serializers.CharField(max_length=100, allow_null=True)
    inicio_amparo_poliza_rce = serializers.DateField(allow_null=True)
    fin_amparo_poliza_rce = serializers.DateField(allow_null=True)
    expedicion_poliza_rce = serializers.DateField(allow_null=True)
    tomador = serializers.CharField(max_length=100, allow_null=True)
    aseguradora = serializers.CharField(max_length=100, allow_null=True)
    fecha_radicacion = serializers.IntegerField(allow_null=True)
    tipo_fecha_radicacion = serializers.ChoiceField(choices=TIPO_FECHA_RADICACION_CONTRATO, allow_null=True)
    fecha_preliquidacion = serializers.DateField(allow_null=True)
    
# serializers para los modelos Nap, Cable, Caja_empalme y Reserva
class NapSerializerS(serializers.Serializer):
    pass

class CableSerializerS(serializers.Serializer):
    pass

class CajaEmpalmeSerializerS(serializers.Serializer):
    pass

class ReservaSerializerS(serializers.Serializer):
    pass
