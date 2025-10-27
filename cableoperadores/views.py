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

from .serializers import CableoperadoresSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CableoperadoresSerializer1
from .supabase_client import supabase # Importa el cliente que creaste
class CableoperadoresCreate(APIView):
    """
    Maneja peticiones GET (listar) y POST (crear) para la tabla 'libros' en Supabase.
    """
    serializer_class = CableoperadoresSerializer1
    permission_classes = [IsAuthenticated]
    # ------------------
    # MANEJAR GET (LISTAR)
    # ------------------
    def get(self, request, format=None):
        
        try:
            # Consulta la tabla 'libros' en Supabase
            res = supabase.table("Cableoperadores").select("*").execute()
            print("Obteniendo datos de Supabase...")
            print(res)
        
            # La respuesta de Supabase viene en un objeto con el campo 'data'
            book_data = res.data
            
            # Opcional: Serializa los datos para asegurar la estructura de salida
            serializer = CableoperadoresSerializer1(data=book_data, many=True)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data)

        except Exception as e:
            print(f"Error al obtener datos de Supabase: {e}")
            return Response({"error": "No se pudieron cargar los datos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ------------------
    # MANEJAR POST (CREAR)
    # ------------------
    def post(self, request, format=None):
        serializer = CableoperadoresSerializer1(data=request.data)
        
        if serializer.is_valid():
            # Los datos ya están validados, se envían directamente a Supabase
            validated_data = serializer.validated_data
            validated_data['ejecutiva'] = request.user.username
            try:
                # Inserta el diccionario validado en Supabase
                supabase.table("Cableoperadores").insert(validated_data).execute()
                return Response({"status": "ok", "msg": "Producto creado con éxito"}, 
                                status=status.HTTP_201_CREATED)
            
            except Exception as e: # <-- Atrapa la excepción de validación (AssertionError)
                print(f"Error al obtener datos de Supabase: {e}") 
            # ... y devuelve 500
            return Response({"error": "No se pudieron cargar los datos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CableoperadorDetailView(APIView):
    """
    Maneja peticiones GET (detalle), PUT (actualizar) y DELETE (eliminar) 
    para un cableoperador específico en Supabase.
    """
    serializer_class = CableoperadoresSerializer1
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        """
        Obtiene un solo cableoperador por su ID (pk).
        """
        try:
            # 1. Consultar a Supabase usando el filtro 'eq' (equals)
            res = supabase.table("Cableoperadores").select("*").eq("id", pk).execute()
            
            # 2. Supabase devuelve 'data' como una lista
            data = res.data
            
            # 3. Verificar si se encontró el registro
            if not data:
                return Response(
                    {"error": "Cableoperador no encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 4. Si se encontró, 'data' es una lista con un solo ítem.
            #    Serializamos solo el primer ítem (data[0]).
            #    (Nota: No usamos 'many=True' aquí)
            serializer = self.serializer_class(data=data[0])
            
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Esto maneja el error 500 si la data de Supabase no coincide con el serializer
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error al obtener detalle de Supabase: {e}")
            return Response(
                {"error": "No se pudo cargar el dato."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def patch(self, request, pk, format=None):
        """
        Actualiza parcialmente un cableoperador por su ID (pk).
        """
        serializer = CableoperadoresSerializer1(data=request.data)
        # 1. Validar los datos entrantes (partial=True permite actualizaciones parciales)
        #    Solo validará los campos que el cliente envíe en el JSON.
        serializer = self.serializer_class(data=request.data, partial=True)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            # Si no se envió ningún dato, no hay nada que actualizar
            if not validated_data:
                return Response(
                    {"error": "No se proporcionaron datos para actualizar."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # 2. Ejecutar el UPDATE en Supabase
                #    Usa .update() con los datos validados y .eq() para el filtro WHERE
                res = supabase.table("Cableoperadores").update(validated_data).eq("id", pk).execute()
                
                # 3. Verificar la respuesta de Supabase
                if res.data:
                    # Devuelve el objeto actualizado (Supabase devuelve una lista)
                    return Response(res.data[0], status=status.HTTP_200_OK)
                else:
                    # Si res.data está vacío, significa que el 'pk' no existía
                    return Response(
                        {"error": "Cableoperador no encontrado para actualizar."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            except Exception as e:
                # Captura errores de Supabase (ej. violación de constraints)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # 4. Si la validación del serializer falla
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)