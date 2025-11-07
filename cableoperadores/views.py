from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from API.permissions import IsGroupMemberForWriteAndDelete
from rest_framework.response import Response
from rest_framework import generics, filters
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.
# views.py

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

class CableoperadoresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadoresSerializer
    permission_classes = [IsGroupMemberForWriteAndDelete]

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5 # Por defecto 20 elementos por página
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
            # Manejar si el ID en la URL no existe (esto generaría un 404/400)
            raise serializers.ValidationError(
                {'cableoperador_pk': 'El Cableoperador especificado en la URL no existe.'}
            )

        # 3. Guardar el objeto, forzando la clave foránea con la instancia de la URL.
        # Esto asegura que la notificación se asigne correctamente, ignorando 
        # (o sobrescribiendo) el 'cableoperador_id' del cuerpo si fuera diferente.
        serializer.save(cableoperador=cableoperador_instance)
