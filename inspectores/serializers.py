from rest_framework import serializers
from .models import *
from cableoperadores.serializers import *
class InspectoresSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Inspectores
        fields = '__all__'