from django.shortcuts import render
from .models import *
from .serializers import *
# Create your views here.
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.response import Response
from cableoperadores.views import CustomLimitOffsetPagination
from django.core.cache import cache

CACHE_TTL = 60 * 15
# Claves de caché
FACTURAS_LIST_CACHE_KEY = 'facturas_list_cache'
REGISTRO_PAGO_LIST_CACHE_KEY = 'registro_pago_list_cache'
# Función auxiliar para invalidar la caché
def invalidate_list_cache(key_prefix):
    cache.clear()
    
# Filtros personalizados pueden ser añadidos aquí si es necesario
class FacturaFilter(django_filters.FilterSet):
    """
    Define filtros exactos y de búsqueda para Facturas.
    Permite filtrar por:
    - estado (exacto)
    - cableoperador (exacto, por ID)
    - search ya está manejado por SearchFilter
    """
    estado = django_filters.CharFilter(
        field_name='estado',
        lookup_expr='iexact'  # Búsqueda insensible a mayúsculas
    )
    cableoperador = django_filters.NumberFilter(
        field_name='cableoperador__id',
        lookup_expr='exact'
    )
    
    class Meta:
        model = Facturacion
        fields = ['estado', 'cableoperador']
# --- FACTURAS ---
class FacturaListCreateView(generics.ListCreateAPIView):
    serializer_class = FacturaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = FacturaFilter
    search_fields = ['cableoperador__id','Num_factura','estado','cableoperador__nombre']
    ordering_fields = ['Fecha_facturacion', 'Mes_uso', 'estado']
    pagination_class = CustomLimitOffsetPagination
    def get_queryset(self):
        """
        Sobrescribe el queryset para filtrar por cableoperador si se provee el parámetro.
        """
        return Facturacion.objects.all().order_by('-Fecha_facturacion')
    def get_cache_key(self, request):
        """Genera una clave de caché única basada en parámetros de paginación, búsqueda y filtros"""
        limit = request.query_params.get('tamaño', 50)
        offset = request.query_params.get('desplazamiento', 0)
        search = request.query_params.get('search', '')
        estado = request.query_params.get('estado', '')
        cableoperador = request.query_params.get('cableoperador', '')
        ordering = request.query_params.get('ordering', '')
        return f"{FACTURAS_LIST_CACHE_KEY}:limit={limit}:offset={offset}:search={search}:estado={estado}:cableoperador={cableoperador}:ordering={ordering}"
    
    # 🚨 NUEVO: Sobrescribimos el método 'list' para manejar la caché manualmente
    def list(self, request, *args, **kwargs):
        # 1. Generar una clave de caché única basada en los parámetros
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)
        
        if cached_data:
            # print(f"DEBUG: Devolviendo lista desde CACHÉ con clave: {cache_key}")
            # Si encontramos datos en caché, los devolvemos directamente
            return Response(cached_data)
        
        # print(f"DEBUG: Generando lista y guardando en CACHÉ con clave: {cache_key}")
        # 2. Si no hay caché, ejecutamos la lógica normal de ListCreateAPIView
        response = super().list(request, *args, **kwargs)
        
        # 3. Guardar la respuesta (los datos) en la caché antes de devolverla
        # Solo cacheamos si la respuesta fue exitosa
        if response.status_code == 200:
            cache.set(cache_key, response.data, CACHE_TTL)
            
        # 4. Devolver la respuesta generada
        return response
    
    # 🚨 Invalidar caché al crear un nuevo Cableoperador
    def perform_create(self, serializer):
        instance = serializer.save()
        # ¡CORRECTO! Esta llamada es la que borra la caché.
        invalidate_list_cache(FACTURAS_LIST_CACHE_KEY)
        return instance
class FacturaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facturacion.objects.all()
    serializer_class = FacturaSerializer

class FacturaByCableoperadorView(generics.ListAPIView):
    """Obtener facturas filtradas por cableoperador"""
    serializer_class = FacturaSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['Fecha_facturacion']

    # def get_queryset(self):
    #     cableoperador_id = self.request.query_params.get('cableoperador_id')
    #     if cableoperador_id:
    #         return Facturacion.objects.filter(
    #             cableoperador=cableoperador_id
    #         )
            # Filtra a través de la relación: Facturacion -> contratos -> cableoperador
    #         return Facturacion.objects.filter(contratos__cableoperador__id=cableoperador_id)
    #     return Facturacion.objects.none()

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