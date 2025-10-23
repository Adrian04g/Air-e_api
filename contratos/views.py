from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
# Create your views here.

class CableoperadorViewSet(generics.ListCreateAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadorSerializer

class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer

