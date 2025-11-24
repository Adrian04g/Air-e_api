from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group

# Create your models here.
# Cableoperadores - Aqui va la tabla de los cableoperadores
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
class Cableoperadores(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre (Obligatorio)')
    nombre_largo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nombre Largo')
    NIT = models.IntegerField(null=True, blank=True)
    Digito_verificacion = models.IntegerField(null=True, blank=True, verbose_name='Digito de verificación')
    RegistroTic = models.BigIntegerField(null=True, blank=True, verbose_name='Registro TIC')
    CodigoInterno = models.BigIntegerField(null=True, blank=True, verbose_name='Codigo Interno')
    pais = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True, verbose_name='Dirección')
    Representante = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.BigIntegerField(verbose_name='Teléfono (Obligatorio)')
    correo = models.EmailField(max_length=100,verbose_name='Correo (Obligatorio)')
    ejecutiva = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=1000, verbose_name='Observaciones (Obligatorio)', null=True, blank=True)
    estado = models.CharField(max_length=100, choices=ESTADOS_CONTRATO, verbose_name='Estado (Obligatorio)')
    vencimiento_factura = models.PositiveIntegerField(null=True, blank=True)
    preliquidacion_num = models.PositiveIntegerField(null=True, blank=True, verbose_name='Preliquidacion Numero')
    preliquidacion_letra = models.CharField(max_length=100,null=True, blank=True, verbose_name='Preliquidacion Letra')
    respuesta_preliquidacion = models.CharField(choices=Rliquidacion, max_length=100,null=True, blank=True, verbose_name='Respuesta Preliquidacion')

    class Meta:
        db_table = "cableoperadores"
    def __str__(self):
        return self.nombre
    
TIPO_NOTIFICACION = [
    ('cobro_multa', 'Cobro de Multa'),
    ('suspension_nuevos_accesos', 'Suspensión de Nuevos Accesos'),
    ('cobro_prejuridico', 'Cobro Prejurídico'),
    ('incumplimiento_pago_factura', 'Incumplimiento de Pago de Factura'),
]
class Notificacion(models.Model):
    cableoperador = models.ForeignKey(Cableoperadores, on_delete=models.CASCADE)
    tipo_notificacion = models.CharField(max_length=100, choices=TIPO_NOTIFICACION, default='cobro_multa')
    fecha = models.DateField()

    def __str__(self):
        return f"Notificación de {self.cableoperador.nombre} - {self.fecha}"