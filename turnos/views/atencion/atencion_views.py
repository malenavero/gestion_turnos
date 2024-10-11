# turnos/views/atencion/atencion_views.py

from datetime import date
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from turnos.models import Especialidad, Medico, Paciente, Turno
from turnos.utils import filtrar_turnos



@login_required
def atencion(request):
    return render(request, 'atencion/atencion.html')


@login_required
def atencion_sala_espera(request, turno_id=None):
    medicos = Medico.objects.all().order_by('apellido', 'nombre')
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')

    # Obtener filtros de la URL
    selected_paciente = request.GET.get('paciente')
    selected_medico = request.GET.get('medico')
    
    # Obtener la fecha actual
    today = date.today()

    query = {
        'paciente_id': selected_paciente,
        'medico_id': selected_medico,
        'fecha': today
    }

    # Filtrar turnos ocupados solo para hoy
    turnos_en_espera = Turno.objects.filter(estado='sala_espera', fecha_hora__date=today)
    turnos_en_espera = filtrar_turnos(turnos_en_espera, query)

    if request.method == 'POST' and turno_id:
        turno = get_object_or_404(Turno, id=turno_id)

        try:
            # Aquí debes agregar la lógica para manejar la solicitud POST
            pass
            
        except ValidationError as e:
            messages.error(request, str(e))

    context = {
        'turnos': turnos_en_espera,
        'pacientes': pacientes,
        'medicos': medicos,
        'selected_paciente': selected_paciente,
        'selected_medico': selected_medico,
        'selected_date': today,
        'error': locals().get('error_message', None),  # Mensaje de error si existe
    }
    return render(request, 'atencion/atencion_sala_espera.html', context)

