from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, filters
from API.permissions import IsGroupMemberForWriteAndDelete
# Importaciones para Caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache # 🚨 IMPORTANTE para invalidar el caché
# Create your views here.

# Tiempo de caché: 15 minutos (900 segundos)
CACHE_TTL = 60 * 15
# Claves de caché (necesarias para invalidación)
CONTRATOS_LIST_CACHE_KEY = 'contratos_list_cache'

# Función auxiliar para invalidar la primera página de la lista (sustituye a delete_pattern)
def invalidate_list_cache(key_prefix):
    # La clave de caché que crea @cache_page es única para la URL + parámetros.
    # Por lo general, la primera página (sin parámetros o con ?page=1) es la más común.
    # Intentamos invalidar la clave de la lista principal.
    
    # 🚨 NOTA: Este es un enfoque de compromiso, ya que no invalida búsquedas ni otras páginas.
    # Si usas un middleware de caché, la clave puede ser compleja. Aquí usamos la clave simple.
    
    # Intenta invalidar la primera página (que suele ser la más solicitada)
    # Ejemplo de clave generada: ':1:views.cableoperador_list_cache:' + md5(url)
    # Dado que no podemos saber la URL exacta, usamos cache.clear() como último recurso 
    # o confiamos en la clave más simple generada por el decorador si conocemos la vista exacta.
    
    # Para simplicidad y evitar delete_pattern, usaremos un enfoque más directo:
    cache.clear() # Intenta eliminar la clave base si existe

@method_decorator(cache_page(CACHE_TTL, key_prefix=CONTRATOS_LIST_CACHE_KEY), name='dispatch')
class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]
    # Habilita búsqueda por texto en campos relevantes. Usar ?search=texto en la URL.
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cableoperador__nombre',
        'estado_contrato',
        'tomador',
        'aseguradora',
    ]
    # 🚨 Invalidar caché al crear un nuevo contrato
    def perform_create(self, serializer):
        instance = serializer.save()
        # FIX: Eliminamos delete_pattern. Solo intentamos invalidar la clave más simple.
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY) 
        return instance
    
class ContratoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]
    def perform_update(self, serializer):
        instance = serializer.save()
        # FIX: Invalidamos la clave base de la lista al actualizar
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)

    # 🚨 Invalidar caché al eliminar un contrato
    def perform_destroy(self, instance):
        instance.delete()
        # FIX: Invalidamos la clave base de la lista al eliminar
        invalidate_list_cache(CONTRATOS_LIST_CACHE_KEY)