# turnos.views.base_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from turnos.models import Turno, Medico
from datetime import timedelta

@login_required
def panel_principal(request):
    return render(request, 'main.html')

def tarea_inicio_diario():
    hoy = timezone.localtime().date()
    ayer = hoy - timedelta(days=1)

    # Marcar los turnos del día anterior como 'ausente' si están en 'ocupado'
    Turno.objects.filter(fecha_hora__date=ayer, estado='ocupado').update(estado='ausente')

    # Eliminar turnos que quedaron disponibles antes de hoy
    Turno.objects.filter(fecha_hora__date__lt=hoy, estado='disponible').delete()

    # Generar turnos para el próximo mes
    if hasattr(Medico, 'generar_turnos'):
        Medico.generar_turnos()


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Comprobar si es el primer login del día
            fecha_ultimo_login = request.session.get('ultimo_login_fecha')
            hoy = timezone.localtime().date()

            if not fecha_ultimo_login or fecha_ultimo_login != str(hoy):
                # Ejecutar la tarea de inicio diario
                tarea_inicio_diario()
                # Actualizar la sesión con la fecha de hoy
                request.session['ultimo_login_fecha'] = str(hoy)
            
            # Redirigir al usuario a la página principal
            return redirect('main')
        else:
            error = "Credenciales incorrectas"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')