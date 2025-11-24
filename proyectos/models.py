from django.db import models
from cableoperadores.models import Cableoperadores
from inspectores.models import Inspectores
# Create your models here.
# Tipo de ingreso del proyecto
class AlturaInicialPoste(models.Model):
    proyecto = models.OneToOneField(
        'IngresoProyecto',
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Proyecto"
    )  # , related_name="altura_inicial_poste")
    tipo8 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 8", default=0
    )
    tipo9 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 9", default=0
    )
    tipo10 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 10", default=0
    )
    tipo11 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 11", default=0
    )
    tipo12 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 12", default=0
    )
    tipo14 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 14", default=0
    )
    tipo16 = models.IntegerField(
        verbose_name="Ingrese cantidad de Poste de Altura 16", default=0
    )
INGRESO = [
    ('Viabilidad', 'Viabilidad'),
    ('Desmonte', 'Desmonte'),
    ('Legalizacion', 'Legalizacion'),
]
ESTADO = [
        ('En_proceso', 'En proceso'),
        ('cancelado', 'Cancelado'),
        ('rechazado_GD', 'Rechazado GD'),
        ('incluir_contrato', 'Incluir en Contrato'),
        ('negado', 'Negado'),
]
# Choices para departamentos
DEPARTAMENTOS = [
    ('atlantico', 'Atlantico'),
    ('magdalena', 'Magdalena'),
    ('la_guajira', 'La Guajira'),
]
class IngresoProyecto(models.Model):
    cableoperador = models.ForeignKey(Cableoperadores, on_delete=models.CASCADE,verbose_name="Cableoperador")
    OT_PRST = models.CharField(max_length=100, verbose_name="OT PRST", null=True, blank=True)
    OT_AIRE = models.CharField(max_length=100, verbose_name="OT Air-e", primary_key=True)
    nombre = models.CharField(max_length=100)
    # 
    rechazado_GD = models.BooleanField(default=False, verbose_name="¿Rechazado GD?")
    cancelado = models.BooleanField(default=False, verbose_name="¿Cancelado?")
    incluir_contrato = models.BooleanField(default=False, verbose_name="¿Incluir en Contrato?")
    negado = models.BooleanField(default=False, verbose_name="¿Negado?")
    #
    TipoIngreso = models.CharField(max_length=100, choices=INGRESO, default='Viabilidad')
    # Informacion de la ubicacion
    departamento = models.CharField(max_length=20,choices=DEPARTAMENTOS)
    municipio = models.CharField(max_length=50,verbose_name="Municipio", null=True, blank=True)
    barrio = models.CharField(max_length=50,verbose_name="Barrio", null=True, blank=True)
    # Fechas
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_confirmacion_fin = models.DateField(null=True, blank=True)
    fecha_radicacion_prst = models.DateField(null=True, blank=True)
    fecha_revision_doc = models.DateField(null=True, blank=True)
    fecha_entrega_coordinador = models.DateField(null=True, blank=True, auto_now_add=True)
    estado_ingreso = models.CharField(max_length=100, choices=ESTADO, default='En_proceso', verbose_name="Registro de estado del proyecto", null=True, blank=True)
    observaciones = models.TextField(max_length=1000, null=True, blank=True)
    class Meta:
        db_table = "ingreso_proyecto"
    def __str__(self):
        return self.OT_AIRE
    
class Cable(models.Model):
    # La clave OneToOneField asegura que solo haya un registro de Cable por Contrato
    proyecto = models.OneToOneField(
        'Proyectos', # Apunta al modelo Proyectos
        on_delete=models.CASCADE, 
        primary_key=True,
        to_field='datos_ingreso',
        verbose_name="Proyecto Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Cables_proyecto"
    def __str__(self):
        return f"Cables de Proyecto {self.proyecto.datos_ingreso.nombre}"

class Caja_empalme(models.Model):
    proyecto = models.OneToOneField(
        'Proyectos', 
        on_delete=models.CASCADE, 
        primary_key=True, 
        to_field='datos_ingreso',
        verbose_name="Proyecto Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Cajas_empalme_proyectos"
    def __str__(self):
        return f"Cajas de Proyecto {self.proyecto.datos_ingreso.nombre}"

class Reserva(models.Model):
    proyecto = models.OneToOneField(
        'Proyectos', 
        on_delete=models.CASCADE, 
        primary_key=True, 
        to_field='datos_ingreso',
        verbose_name="Proyecto Asociado"
    )
    tipo8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tipo10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tipo12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tipo14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tipo15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tipo16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tipo20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Reservas_proyectos"

    def __str__(self):
        return f"Reservas de Proyecto {self.proyecto.datos_ingreso.nombre}"

class Nap(models.Model):
    proyecto = models.OneToOneField(
        'Proyectos', 
        on_delete=models.CASCADE, 
        primary_key=True, 
        to_field='datos_ingreso',
        verbose_name="Proyecto Asociado"
    )
    tip8 = models.PositiveIntegerField(verbose_name="8 metros", default=0)
    tip10 = models.PositiveIntegerField(verbose_name="10 metros", default=0)
    tip12 = models.PositiveIntegerField(verbose_name="12 metros", default=0)
    tip14 = models.PositiveIntegerField(verbose_name="14 metros", default=0)
    tip15 = models.PositiveIntegerField(verbose_name="15 metros", default=0)
    tip16 = models.PositiveIntegerField(verbose_name="16 metros", default=0)
    tip20 = models.PositiveIntegerField(verbose_name="20 metros", default=0)
    class Meta:
        db_table = "Naps_proyectos"

class Proyectos(models.Model):
    datos_ingreso = models.ForeignKey(IngresoProyecto, on_delete=models.CASCADE, to_field='OT_AIRE', db_column='datos_ingreso_id', primary_key=True)
    inspector_responsable = models.ForeignKey(
        Inspectores, 
        on_delete=models.SET_NULL, # O CASCADE, dependiendo de tu lógica
        null=True, 
        blank=True,
        verbose_name="Inspector Responsable"
    )
    estado_actual = models.CharField(max_length=100)
    fecha_inspeccion = models.DateField()
    fecha_analisis_inspeccion = models.DateField()
    class Meta:
        db_table = "Proyectos"
    def __str__(self):
        return f"Proyecto {self.datos_ingreso.OT_AIRE}"
    