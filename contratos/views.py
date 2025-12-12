from .models import Contratos, Nap
from .serializers import *
from rest_framework import generics, filters
from rest_framework.response import Response
from API.permissions import IsGroupMemberForWriteAndDelete
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
# Importaciones para Caching
from django.core.cache import cache
from cableoperadores.views import CustomLimitOffsetPagination

# Tiempo de caché: 15 minutos (900 segundos)
CACHE_TTL = 60 * 15
# Claves de caché
CONTRATOS_LIST_CACHE_KEY = 'contratos_list_cache'


# Función auxiliar para invalidar la caché
def invalidate_list_cache(key_prefix):
    cache.clear()


# Clase de filtros personalizada para Contratos
class ContratoFilter(django_filters.FilterSet):
    """
    Define filtros exactos y de búsqueda para Contratos.
    Permite filtrar por:
    - estado_contrato (exacto)
    - cableoperador (exacto, por ID)
    - search ya está manejado por SearchFilter
    """
    estado_contrato = django_filters.CharFilter(
        field_name='estado_contrato',
        lookup_expr='iexact'  # Búsqueda insensible a mayúsculas
    )
    cableoperador = django_filters.NumberFilter(
        field_name='cableoperador__id',
        lookup_expr='exact'
    )
    
    class Meta:
        model = Contratos
        fields = ['estado_contrato', 'cableoperador']


class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]
    pagination_class = CustomLimitOffsetPagination
    
    # Habilita búsqueda, filtrado y ordenamiento
    filter_backends = [
        DjangoFilterBackend,      # Para filtros exactos (estado_contrato, cableoperador)
        filters.SearchFilter,      # Para búsqueda por texto (search)
        filters.OrderingFilter     # Para ordenamiento
    ]
    
    # Clase de filtros personalizada
    filterset_class = ContratoFilter
    
    # Campos para búsqueda con ?search=texto
    search_fields = [
        'cableoperador__nombre',
        'cableoperador__nombre_largo',
        'tomador',
        'aseguradora',
    ]
    
    # Campos permitidos para ordenamiento con ?ordering=campo
    ordering_fields = [
        'id',
        'inicio_vigencia',
        'fin_vigencia',
        'valor_contrato',
        'estado_contrato'
    ]

    def get_cache_key(self, request):
        """
        Genera una clave de caché única basada en todos los parámetros:
        paginación, búsqueda, filtros y ordenamiento.
        """
        limit = request.query_params.get('tamaño', 50)
        offset = request.query_params.get('desplazamiento', 0)
        search = request.query_params.get('search', '')
        ordering = request.query_params.get('ordering', '')
        estado_contrato = request.query_params.get('estado_contrato', '')
        cableoperador = request.query_params.get('cableoperador', '')
        
        return (
            f"{CONTRATOS_LIST_CACHE_KEY}:limit={limit}:offset={offset}"
            f":search={search}:ordering={ordering}"
            f":estado={estado_contrato}:cableop={cableoperador}"
        )

    def list(self, request, *args, **kwargs):
        # 1. Generar una clave de caché única
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # 2. Si no hay caché, ejecutar la lógica normal
        response = super().list(request, *args, **kwargs)

        # 3. Guardar en caché si fue exitoso
        if response.status_code == 200:
            cache.set(cache_key, response.data, CACHE_TTL)

        return response

    def perform_create(self, serializer):
        instance = serializer.save()
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)
        return instance
    def perform_update(self, serializer):
        instance = serializer.save()
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)
        return instance
    def perform_destroy(self, instance):
        instance.delete()
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)

class ContratoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]

    def perform_update(self, serializer):
        serializer.save()
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)

class NapView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nap.objects.all()
    serializer_class = NapSerializer