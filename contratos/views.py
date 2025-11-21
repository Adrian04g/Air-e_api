from .models import Contratos, Nap
from .serializers import *
from rest_framework import generics, filters
from rest_framework.response import Response
from API.permissions import IsGroupMemberForWriteAndDelete
# Importaciones para Caching
from django.core.cache import cache  # ¡IMPORTANTE para invalidar el caché!

# Create your views here.
# Tiempo de caché: 15 minutos (900 segundos)
CACHE_TTL = 60 * 15
# Claves de caché (necesarias para invalidación)
CONTRATOS_LIST_CACHE_KEY = 'contratos_list_cache'


# Función auxiliar para invalidar la caché (sustituye a delete_pattern)
def invalidate_list_cache(key_prefix):
    cache.clear()  # Intenta eliminar la clave base si existe


class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]
    # Habilita búsqueda y ordenamiento. Usar ?search=texto y ?ordering=campo
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'cableoperador__nombre',
        'estado_contrato',
        'tomador',
        'aseguradora',
    ]

    def get_cache_key(self, request):
        """
        Genera una clave de caché única basada en parámetros de paginación,
        búsqueda y ordenamiento.
        """
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        search = request.query_params.get('search', '')
        ordering = request.query_params.get('ordering', '')
        return (
            f"{CONTRATOS_LIST_CACHE_KEY}:limit={limit}:offset={offset}"
            f":search={search}:ordering={ordering}"
        )

    def list(self, request, *args, **kwargs):
        # 1. Generar una clave de caché única basada en los parámetros
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)

        if cached_data:
            # Si encontramos datos en caché, los devolvemos directamente
            return Response(cached_data)

        # 2. Si no hay caché, ejecutamos la lógica normal de ListCreateAPIView
        response = super().list(request, *args, **kwargs)

        # 3. Guardar la respuesta (los datos) en la caché antes de devolverla
        # Solo cacheamos si la respuesta fue exitosa
        if response.status_code == 200:
            cache.set(cache_key, response.data, CACHE_TTL)

        # 4. Devolver la respuesta generada
        return response

    # 🚨 Invalidar caché al crear un nuevo contrato
    def perform_create(self, serializer):
        instance = serializer.save()
        # FIX: Invalidamos la caché de la lista al crear.
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)
        return instance


class ContratoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]

    def perform_update(self, serializer):
        serializer.save()
        # FIX: Invalidamos la clave base de la lista al actualizar
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)

    # 🚨 Invalidar caché al eliminar un contrato
    def perform_destroy(self, instance):
        instance.delete()
        # FIX: Invalidamos la clave base de la lista al eliminar
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)


class NapView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nap.objects.all()
    serializer_class = NapSerializer