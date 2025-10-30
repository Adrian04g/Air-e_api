from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# En tu archivo views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer # Importa el serializador que creaste

class UserProfileView(APIView):
    # Esto asegura que solo se procesarán peticiones con un token JWT válido.
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # request.user contiene la instancia del usuario que fue identificada
        # por el token JWT.
        serializer = UserSerializer(request.user)
        # Devolver los datos serializados
        return Response(serializer.data)