from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from API.permissions import IsGroupMemberForWriteAndDelete
from rest_framework.response import Response
from rest_framework import generics, filters, serializers
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
# Importaciones para Caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache # ¡IMPORTANTE para invalidar el caché!

# Tiempo de caché: 15 minutos (900 segundos)
CACHE_TTL = 60 * 15
# Claves de caché (necesarias para invalidación)
CABLEOPERADORES_LIST_CACHE_KEY = 'cableoperadores_list_cache' 
# Create your views here.
# views.py
def invalidate_list_cache(key_prefix):
    cache.clear() # Intenta eliminar la clave base si existe
class DatosProtegidos(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden acceder

    def get(self, request):
        # request.user ahora es el usuario autenticado
        return Response({"mensaje": f"Hola {request.user.username}, tienes acceso."})
    
class CableoperadoresList(generics.ListCreateAPIView):
    # Devolver por defecto ordenado alfabéticamente por nombre_largo
    queryset = Cableoperadores.objects.all().order_by('nombre_largo')
    serializer_class = CableoperadoresSerializer
    permission_classes = [IsAuthenticated]
    # Habilita búsqueda por texto en campos relevantes. Usar ?search=texto en la URL.
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'nombre',
        'ciudad',
        'direccion',
        'NIT',
        'correo',
    ]
    
    # 🚨 NUEVO: Sobrescribimos el método 'list' para manejar la caché manualmente
    def list(self, request, *args, **kwargs):
        # 1. Intentar obtener la lista de la caché
        # Usamos una clave simple. Si usas paginación/búsqueda, la clave debe ser más compleja.
        # Por ahora, esta clave simple funcionará para la lista principal.
        cached_data = cache.get(CABLEOPERADORES_LIST_CACHE_KEY)
        
        if cached_data:
            # print("DEBUG: Devolviendo lista desde CACHÉ")
            # Si encontramos datos en caché, los devolvemos directamente
            return Response(cached_data)
        
        # print("DEBUG: Generando lista y guardando en CACHÉ")
        # 2. Si no hay caché, ejecutamos la lógica normal de ListCreateAPIView
        response = super().list(request, *args, **kwargs)
        
        # 3. Guardar la respuesta (los datos) en la caché antes de devolverla
        # Solo cacheamos si la respuesta fue exitosa
        if response.status_code == 200:
            cache.set(CABLEOPERADORES_LIST_CACHE_KEY, response.data, CACHE_TTL)
            
        # 4. Devolver la respuesta generada
        return response
    
    # 🚨 Invalidar caché al crear un nuevo Cableoperador
    def perform_create(self, serializer):
        instance = serializer.save()
        # ¡CORRECTO! Esta llamada es la que borra la caché.
        invalidate_list_cache(CABLEOPERADORES_LIST_CACHE_KEY)
        return instance

class CableoperadoresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadoresSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]

    # 🚨 Invalidar caché al actualizar un Cableoperador
    def perform_update(self, serializer):
        instance = serializer.save()
        # ¡CORRECTO! Esta llamada es la que borra la caché.
        invalidate_list_cache(CABLEOPERADORES_LIST_CACHE_KEY)
        return instance # Devuelve la instancia guardada

    # 🚨 Invalidar caché al eliminar un Cableoperador
    def perform_destroy(self, instance):
        instance.delete()
        # ¡CORRECTO! Esta llamada es la que borra la caché.
        invalidate_list_cache(CABLEOPERADORES_LIST_CACHE_KEY)

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5 # Por defecto 5 elementos por página (cambiado de 20)
    #max_limit = 50     # Límite máximo que el cliente puede solicitar
    limit_query_param = 'tamaño' # Cambia el nombre del parámetro de consulta (ej. ?offset=0&tamaño=15)
    offset_query_param = 'desplazamiento'

class NotificacionList(generics.ListCreateAPIView):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['cableoperador__nombre']

class NotificacionListByCableoperador(generics.ListCreateAPIView):
    serializer_class = NotificacionSerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        cableoperador_pk = self.kwargs['cableoperador_pk']
        return Notificacion.objects.filter(cableoperador_id=cableoperador_pk).order_by('-fecha')
    
    def perform_create(self, serializer):
        # 1. Obtener el ID del cableoperador desde la URL (kwargs)
        cableoperador_id = self.kwargs.get('cableoperador_pk')
        
        # 2. Obtener la instancia del Cableoperador
        try:
            cableoperador_instance = Cableoperadores.objects.get(pk=cableoperador_id)
        except Cableoperadores.DoesNotExist:
            # Manejar si el ID en la URL no existe
            raise serializers.ValidationError(
                {'cableoperador_pk': 'El Cableoperador especificado en la URL no existe.'}
            )

        # 3. Guardar el objeto, forzando la clave foránea con la instancia de la URL.
        serializer.save(cableoperador=cableoperador_instance)