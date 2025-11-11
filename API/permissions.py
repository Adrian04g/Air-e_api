from rest_framework import permissions

class IsGroupMemberForWriteAndDelete(permissions.BasePermission):
    """
    Permite el acceso de solo lectura (GET) a usuarios autenticados.
    Permite acciones de escritura/borrado (PUT, PATCH, DELETE)
    solo a usuarios que pertenecen a los grupos requeridos.
    """
    # Define el nombre(s) del grupo(s) requerido(s) para escribir/borrar
    required_groups = ['Administradores', 'Ejecutivas'] 
    
    def has_permission(self, request, view):
        user = request.user
        
        # 1. PERMISOS DE LECTURA (GET, HEAD, OPTIONS)
        # Permite la lectura solo si el usuario está autenticado.
        if request.method in permissions.SAFE_METHODS:
            return user.is_authenticated 
        
        # 2. PERMISOS DE ESCRITURA/BORRADO (PUT, PATCH, DELETE)
        # Si la solicitud no es de lectura, el usuario DEBE estar autenticado.
        if not user.is_authenticated:
            return False

        # Verifica si el usuario pertenece al grupo(s) requerido(s).
        # Esto aplica para PUT, PATCH, y DELETE.
        is_member = user.groups.filter(name__in=self.required_groups).exists()
        
        return is_member