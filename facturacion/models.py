from django.db import models
from indexapp.models import Cableoperadores
# Create your models here.
SI_NO = [
    ('si' , 'Sí'),
    ('no' , 'No'),
]
class Facturacion(models.Model):
    Nombre_prst = models.ForeignKey(Cableoperadores, on_delete=models.CASCADE, verbose_name='Nombre del Prestador')
    Responsable = models.CharField(max_length=100, verbose_name='Responsable')
    Mes_uso = models.DateField(verbose_name='Mes de Uso')
    Fecha_fact = models.DateField(verbose_name='Fecha de Facturación')
    Num_fact = models.CharField(max_length=50, verbose_name='Número de Factura', unique=True)
    Valor_iva = models.FloatField(max_length= 50, verbose_name='Valor IVA')
    Valor_iva_millones = models.FloatField(verbose_name='Valor en millones')
    Fecha_venc = models.DateField(verbose_name='Fecha de Vencimiento')
    Periodo_venc = models.DateField(verbose_name='Periodo de Vencimiento')
    Factura_aceptada = models.CharField(max_length=50,choices=SI_NO, verbose_name='Factura aceptada')
    Factura_vencida = models.CharField(max_length=50,choices=SI_NO, verbose_name='Vencida')
    Factura_CRC = models.CharField(max_length=50,choices=SI_NO,  verbose_name='Facturado CRC')
    Valor_pagado = models.FloatField(verbose_name='Valor Pagado')
    Fecha_pago = models.DateField(verbose_name='Fecha pago')
    Periodo_pago = models.DateField(verbose_name='Periodo pago')
    Fecha_aplicacion = models.DateField(max_length=50, verbose_name='Fecha de aplicacion')
    Fecha_confirmacion = models.DateField(blank=True, null=True, verbose_name='Fecha de confirmacion')
    Valor_deuda = models.FloatField(verbose_name='Valor deuda')
    Pagado = models.CharField(max_length=50,choices=SI_NO, verbose_name='Pagado?')
    Observciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    Interes_iva = models.CharField(max_length=50,choices=SI_NO, verbose_name='Interes IVA')
    Indicador_recaudo = models.DateField(verbose_name='Inducador de recaudo')
    Acuerdo_pago = models.CharField(max_length=50,choices=SI_NO, verbose_name='Acuerdo de pago?')
    Fecha_acuerdo_pago = models.DateField(verbose_name='Fecha de acuerdo de pago', null=True, blank=True)
    Fecha_pago_AP = models.DateField(verbose_name='Fecha de pago acuerdo de pago', null=True, blank=True)
    
    
    def __str__(self):
        return self.Num_fact
    class Meta:
        db_table = 'Facturacion'