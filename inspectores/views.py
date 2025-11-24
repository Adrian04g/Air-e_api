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

class InspectoresView(generics.ListCreateAPIView):
    queryset = Inspectores.objects.all()
    serializer_class = InspectoresSerializer
class SingleInspectoresView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inspectores.objects.all()
    serializer_class = InspectoresSerializer