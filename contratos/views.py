from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, filters

# Create your views here.

class CableoperadorViewSet(generics.ListCreateAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadorSerializer

class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer
    # Habilita búsqueda por texto en campos relevantes. Usar ?search=texto en la URL.
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cableoperador__nombre',
        'estado_contrato',
        'tomador',
        'aseguradora',
    ]
    
class ContratoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer