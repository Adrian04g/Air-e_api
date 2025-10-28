from django.shortcuts import render
from .models import *
from .serializers import *
from .serializersS import *
from rest_framework import generics
from rest_framework.views import APIView
# Create your views here.

class CableoperadorViewSet(generics.ListCreateAPIView):
    queryset = Cableoperadores.objects.all()
    serializer_class = CableoperadorSerializer

class ContratoViewSet(generics.ListCreateAPIView):
    queryset = Contratos.objects.all()
    serializer_class = ContratoSerializer


from rest_framework.response import Response
from rest_framework import status
from cableoperadores.supabase_client import supabase
class ContratoSupabase(APIView):
    serializer_class = ContratoSerializerS
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # Consulta la tabla 'libros' en Supabase
            res = supabase.table("Contratos").select("*").execute()
            print("Obteniendo datos de Supabase...")

        
            # La respuesta de Supabase viene en un objeto con el campo 'data'
            book_data = res.data
            
            # Opcional: Serializa los datos para asegurar la estructura de salida
            serializer = ContratoSerializerS(data=book_data, many=True)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data)

        except Exception as e:
            print(f"Error al obtener datos de Supabase: {e}")
            return Response({"error": "No se pudieron cargar los datos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, *args, **kwargs):
        serializer = ContratoSerializerS(data=request.data)
        if serializer.is_valid():
            # Los datos ya están validados, se envían directamente a Supabase
            validated_data = serializer.validated_data
            
            try:
                # Inserta el diccionario validado en Supabase
                supabase.table("Contratos").insert(validated_data).execute()
                return Response({"status": "ok", "msg": "Producto creado con éxito"}, 
                                status=status.HTTP_201_CREATED)
            
            except Exception as e: # <-- Atrapa la excepción de validación (AssertionError)
                print(f"Error al obtener datos de Supabase: {e}") 
            # ... y devuelve 500
            return Response({"error": "No se pudieron cargar los datos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ContratoDetail(APIView):
    serializer_class = ContratoSerializerS
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        """
        Obtiene un solo cableoperador por su ID (pk).
        """
        try:
            # 1. Consultar a Supabase usando el filtro 'eq' (equals)
            res = supabase.table("Contratos").select("*").eq("id", pk).execute()
            
            # 2. Supabase devuelve 'data' como una lista
            data = res.data
            
            # 3. Verificar si se encontró el registro
            if not data:
                return Response(
                    {"error": "Contrato no encontrado."},
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
    def post(self, request, *args, **kwargs):
        serializer = ContratoSerializerS(data=request.data)
        if serializer.is_valid():
            # Los datos ya están validados, se envían directamente a Supabase
            validated_data = serializer.validated_data
            
            try:
                # Inserta el diccionario validado en Supabase
                supabase.table("Contratos").insert(validated_data).execute()
                return Response({"status": "ok", "msg": "Producto creado con éxito"}, 
                                status=status.HTTP_201_CREATED)
            
            except Exception as e: # <-- Atrapa la excepción de validación (AssertionError)
                print(f"Error al obtener datos de Supabase: {e}") 
            # ... y devuelve 500
            return Response({"error": "No se pudieron cargar los datos"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)