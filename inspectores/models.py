from django.db import models
from django.contrib.auth.models import User

class Inspectores(models.Model):
    # Enlace UNO a UNO con el usuario de Django.
    # on_delete=models.CASCADE asegura que si el usuario se borra, también se borra el perfil.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campo para información adicional del técnico/inspector
    especialidad = models.CharField(max_length=100, blank=True)
    
    # Puedes añadir más campos relevantes aquí...
    
    def __str__(self):
        # Muestra el nombre completo del usuario en el Admin y formularios
        return self.user.get_full_name() or self.user.username