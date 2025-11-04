from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, filters
from .models import Cableoperadores
from .serializers import CableoperadoresSerializer
from django.contrib.auth.models import User

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
    permission_classes = [IsAuthenticated]