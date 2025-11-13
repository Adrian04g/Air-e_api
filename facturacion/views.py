from django.shortcuts import render
from .models import *
from .serializers import *
# Create your views here.
from rest_framework import generics, filters


# --- FACTURAS ---
class FacturaListCreateView(generics.ListCreateAPIView):
    queryset = Facturacion.objects.all().order_by('-Fecha_facturacion')
    serializer_class = FacturaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Num_factura', 'contratos__cableoperador__nombre']
    

class FacturaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facturacion.objects.all()
    serializer_class = FacturaSerializer

# class FacturaByCableoperadorView(generics.ListAPIView):
#     """Obtener facturas filtradas por cableoperador"""
#     serializer_class = FacturaSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['Fecha_facturacion']

#     def get_queryset(self):
#         cableoperador_id = self.request.query_params.get('cableoperador_id')
#         if cableoperador_id:
#             return Facturacion.objects.filter(
#                 contratos__cableoperador__id=cableoperador_id
#             )
#         return Facturacion.objects.none()

# --- REGISTROS DE PAGO ---
class RegistroPagoListCreateView(generics.ListCreateAPIView):
    queryset = registro_pago.objects.all()
    serializer_class = RegistroPagoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['facturacion__Num_factura']
    ordering_fields = ['fecha_pago']

class RegistroPagoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = registro_pago.objects.all()
    serializer_class = RegistroPagoSerializer

# class RegistroPagoByFacturaView(generics.ListAPIView):
#     """Obtener pagos filtrados por factura"""
#     serializer_class = RegistroPagoSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['fecha_pago']

#     def get_queryset(self):
#         factura_id = self.request.query_params.get('factura_id')
#         if factura_id:
#             return registro_pago.objects.filter(facturacion__id=factura_id)
#         return registro_pago.objects.none()