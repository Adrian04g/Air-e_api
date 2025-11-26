from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, filters
from rest_framework.response import Response
from API.permissions import IsGroupMemberForWriteAndDelete
# Importaciones para Caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache # ¡IMPORTANTE para invalidar el caché!
# Create your views here.

class IngresoProyectoView(generics.ListCreateAPIView):
    queryset = IngresoProyecto.objects.all().order_by('-fecha_radicacion_prst')
    serializer_class = IngresoProyectoSerializer

class SingleIngresoProyectoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngresoProyecto.objects.all()
    serializer_class = IngresoProyectoSerializer

class ProyectosView(generics.ListCreateAPIView):
    queryset = Proyectos.objects.all()
    serializer_class = ProyectosSerializer
    
class SingleProyectoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyectos.objects.all()
    serializer_class = ProyectosSerializer

class IngresosNoVinculadosListView(generics.ListAPIView):
    queryset = IngresoProyecto.objects.filter(proyectos__isnull=True)
    serializer_class = IngresoProyectoSerializer