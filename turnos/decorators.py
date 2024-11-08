
from functools import wraps
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def group_required(*group_names):
    """
    Decorador que permite el acceso a usuarios que pertenezcan a uno de los grupos especificados
    o que sean parte del grupo 'Admin'.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Asegura que el usuario esté autenticado
        def _wrapped_view(request, *args, **kwargs):
            # Permitir siempre acceso a los usuarios en el grupo 'Admin'
            if request.user.groups.filter(name='Admin').exists():
                return view_func(request, *args, **kwargs)
            
            # Verificar si el usuario pertenece a uno de los grupos requeridos
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            
            # Renderizar la página 403 si no tiene permisos
            return render(request, '403.html', status=403)
        
        return _wrapped_view
    return decorator