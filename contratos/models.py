from django.db import models
from cableoperadores.models import Cableoperadores
from django.core.exceptions import ValidationError
# Create your models here.
class Cable(models.Model):
    # La clave OneToOneField asegura que solo haya un registro de Cable por Contrato
    contrato = models.OneToOneField(
        'Contratos', # Apunta al modelo Contratos
        on_delete=models.CASCADE, 
        primary_key=True, # Hace que este campo sea la PK, forzando la unicidad
        verbose_name="Contrato Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Cables"
    def __str__(self):
        return f"Cables de Contrato {self.contrato.numero_contrato}"

class Caja_empalme(models.Model):
    contrato = models.OneToOneField(
        'Contratos', 
        on_delete=models.CASCADE, 
        primary_key=True,
        verbose_name="Contrato Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Cajas_empalme"
    def __str__(self):
        return f"Cajas de Contrato {self.contrato.numero_contrato}"

class Reserva(models.Model):
    contrato = models.OneToOneField(
        'Contratos', 
        on_delete=models.CASCADE, 
        primary_key=True,
        verbose_name="Contrato Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Reservas"

    def __str__(self):
        return f"Reservas de Contrato {self.contrato.numero_contrato}"

class Nap(models.Model):
    contrato = models.OneToOneField(
        'Contratos', 
        on_delete=models.CASCADE, 
        primary_key=True,
        verbose_name="Contrato Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Naps"

# Definiciones de Choices
CLASIFICACION = [
    ('tipo1' , 'tipo1'),
    ('tipo2' , 'tipo2'),
    ('tipo3' , 'tipo3'),
]
ESTADOS_CONTRATO = [
    ('Vigente' , 'Vigente'),
    ('Vencido' , 'Vencido'),
    ('Pendiente' , 'Pendiente'),
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
MONTO_ASEGURADO_POLIZA_CHOICES = [
    ('15%_valor_contrato', '15% Valor del Contrato'),
    ('20%_valor_contrato', '20% Valor del Contrato'),
    ('30%_valor_contrato', '30% Valor del Contrato'),
    ('20%_valor_base_constitucion_poliza', '20% Valor base de Constitución de Póliza'),
    ('30%_valor_base_constitucion_poliza', '30% Valor base de Constitución de Póliza'),
    ('no_inferior_100_SMLMV', 'No inferior a 100 SMLMV'),
    ('no_inferior_200_SMLMV', 'No inferior a 200 SMLMV'),
    ('no_inferior_300_SMLMV', 'No inferior a 300 SMLMV'),
]
class Contratos(models.Model):
    cableoperador = models.ForeignKey(Cableoperadores, on_delete=models.PROTECT)
    estado_contrato = models.CharField(max_length=100, choices=ESTADOS_CONTRATO, verbose_name="Estado de Contrato")
    duracion_anos = models.IntegerField(verbose_name="Duración en años", default=0)
    inicio_vigencia = models.DateField(blank=True, null=True)
    fin_vigencia = models.DateField(blank=True, null=True)
    valor_contrato = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Valor del Contrato", default=0)
    # Campos para la Póliza de Cumplimiento
    numero_poliza_cumplimiento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de Póliza")
    vigencia_amparo_poliza_cumplimiento = models.CharField(max_length=100, blank=True, null=True, choices=VIGENCIA_AMPARO_CHOICES, verbose_name="Vigencia de Amparo")
    inicio_vigencia_poliza_cumplimiento = models.DateField(blank=True, null=True, verbose_name="Inicio de Vigencia")
    fin_vigencia_poliza_cumplimiento = models.DateField(blank=True, null=True, verbose_name="Fin de Vigencia")
    monto_asegurado_poliza_cumplimiento = models.CharField(max_length=100, blank=True, null=True, choices=MONTO_ASEGURADO_POLIZA_CHOICES, verbose_name="Monto Asegurado")
    valor_monto_asegurado_poliza_cumplimiento = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name="Valor del Monto Asegurado")
    valor_asegurado_poliza_cumplimiento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Valor Asegurado")
    inicio_amparo_poliza_cumplimiento = models.DateField(blank=True, null=True, verbose_name="Inicio de Amparo")
    fin_amparo_poliza_cumplimiento = models.DateField(blank=True, null=True, verbose_name="Fin de Amparo")
    expedicion_poliza_cumplimiento = models.DateField(blank=True, null=True, verbose_name="Expedición de Póliza")
    # Campos para la Póliza de RCE
    numero_poliza_rce = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de Póliza")
    vigencia_amparo_poliza_rce = models.CharField(max_length=100, blank=True, null=True, choices=VIGENCIA_AMPARO_CHOICES, verbose_name="Vigencia de Amparo")
    inicio_vigencia_poliza_rce = models.DateField(blank=True, null=True, verbose_name="Inicio de Vigencia")
    fin_vigencia_poliza_rce = models.DateField(blank=True, null=True, verbose_name="Fin de Vigencia")
    monto_asegurado_poliza_rce = models.CharField(max_length=100, blank=True, null=True, choices=MONTO_ASEGURADO_POLIZA_CHOICES, verbose_name="Monto Asegurado")
    valor_monto_asegurado_poliza_rce = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name="Valor del Monto Asegurado")
    valor_asegurado_poliza_rce = models.CharField(max_length=100, blank=True, null=True, verbose_name="Valor Asegurado")
    inicio_amparo_poliza_rce = models.DateField(blank=True, null=True, verbose_name="Inicio de Amparo")
    fin_amparo_poliza_rce = models.DateField(blank=True, null=True, verbose_name="Fin de Amparo")
    expedicion_poliza_rce = models.DateField(blank=True, null=True, verbose_name="Expedición de Póliza")
    tomador = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tomador")
    aseguradora = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aseguradora")
    fecha_radicacion = models.CharField(max_length=100, verbose_name="Fecha de Radicación", blank=True, null=True)
    tipo_fecha_radicacion = models.CharField(max_length=100, choices=TIPO_FECHA_RADICACION_CONTRATO, verbose_name="Tipo de Fecha de Radicación", blank=True, null=True)
    fecha_preliquidacion = models.DateField(blank=True, null=True, verbose_name="Fecha de Preliquidación")
    def clean(self):
        """
        Aplica la regla de negocio: solo puede haber un contrato 'Vigente' 
        por cada Cableoperador.
        """
        if self.estado_contrato == 'Vigente':
            
            # Buscar si YA existe un contrato 'Vigente' para este Cableoperador
            vigente_exists = Contratos.objects.filter(
                estado_contrato='Vigente', 
                cableoperador=self.cableoperador # Restringe por Cableoperador
            )
            
            # Excluir la instancia actual (importante para la edición)
            if self.pk:
                vigente_exists = vigente_exists.exclude(pk=self.pk)
            
            if vigente_exists.exists():
                raise ValidationError(
                    {'estado_contrato': 'Este Cableoperador ya tiene un contrato marcado como "Vigente".'}
                )
    class Meta: 
        db_table = "Contratos"
    
    def __str__(self):
        return f"Contrato de {self.cableoperador.nombre} {self.estado_contrato}"