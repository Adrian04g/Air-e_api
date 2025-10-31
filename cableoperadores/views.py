from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
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
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadoresSerializer
    permission_classes = [IsAuthenticated]

class CableoperadoresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadoresSerializer
    permission_classes = [IsAuthenticated]