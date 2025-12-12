from django.db import models
from cableoperadores.models import Cableoperadores
from contratos.models import Contratos
# Create your models here.
SI_NO = [
    ('si' , 'Sí'),
    ('no' , 'No'),
]
class Facturacion(models.Model):
    cableoperador = models.ForeignKey(Cableoperadores, on_delete=models.CASCADE, default=1)
    Mes_uso = models.DateField(verbose_name='Mes de Uso')
    Fecha_facturacion = models.DateField(verbose_name='Fecha de Facturación')
    Num_factura = models.CharField(max_length=50, verbose_name='Número de Factura')
    Valor_facturado_iva = models.FloatField(max_length= 50, verbose_name='Valor IVA')
    Valor_iva_millones = models.FloatField(verbose_name='Valor en millones')
    Fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
    Periodo_vencimiento = models.DateField(verbose_name='Periodo de Vencimiento')
    # Estado de la Factura
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('PagadaParcial', 'Pago Parcial'),
        ('Pagada', 'Pagada'),
        ('Anulada', 'Anulada'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        verbose_name='Estado de Pago'
    )
    Factura_aceptada = models.BooleanField(default=True, verbose_name='Factura Aceptada')
    Factura_CRC = models.BooleanField(default=False, verbose_name='Factura CRC')
    Fecha_aplicacion = models.DateField(max_length=50, verbose_name='Fecha de aplicacion', blank=True, null=True)
    Fecha_confirmacion = models.DateField(blank=True, null=True, verbose_name='Fecha de confirmacion')
    #monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Total', default=0.00)
    # Este campo se calcula dinámicamente o se actualiza al registrar pagos
    #monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Monto Pendiente')
    # Valor_deuda = models.FloatField(verbose_name='Valor deuda')
    # Pagado = models.CharField(max_length=50,choices=SI_NO, verbose_name='Pagado?')
    # Observciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    # Interes_iva = models.CharField(max_length=50,choices=SI_NO, verbose_name='Interes IVA')
    # Indicador_recaudo = models.DateField(verbose_name='Inducador de recaudo')
    # Acuerdo_pago = models.CharField(max_length=50,choices=SI_NO, verbose_name='Acuerdo de pago?')
    # Fecha_acuerdo_pago = models.DateField(verbose_name='Fecha de acuerdo de pago', null=True, blank=True)
    # Fecha_pago_AP = models.DateField(verbose_name='Fecha de pago acuerdo de pago', null=True, blank=True)
    
    
    def __str__(self):
        return f"Factura {self.Num_factura} - {self.cableoperador.nombre} - {self.pk}"
    class Meta:
        db_table = 'Facturacion'
        
class registro_pago(models.Model):
    facturacion = models.ForeignKey(Facturacion, related_name='pagos', on_delete=models.CASCADE)
    fecha_pago = models.DateField(verbose_name='Fecha pago')
    periodo_pago = models.DateField(verbose_name='Periodo pago')
    monto_pagado = models.DecimalField(max_digits=20, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Registro de pago para {self.facturacion.Num_factura} - {self.fecha_pago}"

    class Meta:
        db_table = 'Registro_pago'
        
# class registro_acuerdo_pago(models.Model):
#     facturacion = models.ForeignKey(Facturacion, on_delete=models.CASCADE)
#     fecha_acuerdo = models.DateField(verbose_name='Fecha de Acuerdo')
#     monto_acuerdo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto del Acuerdo')
#     fecha_pago_acuerdo = models.DateField(verbose_name='Fecha de Pago del Acuerdo', null=True, blank=True)
#     observaciones = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Acuerdo de pago para {self.facturacion.Num_factura} - {self.fecha_acuerdo}"

#     class Meta:
#         db_table = 'Registro_acuerdo_pago'
