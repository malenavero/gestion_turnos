# turnos.views.gestion_turnos_views.py

from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from turnos.models import Especialidad, Medico, Paciente, Turno
from turnos.utils import filtrar_turnos

@login_required
def gestion_turnos(request):
    return render(request, 'gestion_turnos/gestion_turnos.html')

@login_required
def turnero(request):
    return render(request, 'gestion_turnos/turnero.html')

@login_required
def turnero_reservar(request):
    medicos = Medico.objects.all().order_by('apellido', 'nombre')
    especialidades = Especialidad.objects.all().order_by('nombre')
    pacientes = list(Paciente.objects.all().order_by('apellido', 'nombre').values('id', 'nombre', 'apellido'))

    # Obtener filtros de la URL
    selected_especialidad = request.GET.get('especialidad')
    selected_medico = request.GET.get('medico')
    selected_date = request.GET.get('fecha')

    
    query = {
        'especialidad_id': selected_especialidad,
        'medico_id': selected_medico,
        'fecha': selected_date
    }

    # Filtrar turnos disponibles
    turnos_disponibles = Turno.objects.filter(estado='disponible')
    turnos_disponibles = filtrar_turnos(turnos_disponibles, query)

    if request.method == 'POST':
        turno_id = request.POST.get('turno_id')
        paciente_id = request.POST.get('paciente_id')
        turno = get_object_or_404(Turno, id=turno_id)
        paciente = get_object_or_404(Paciente, id=paciente_id)

        try:
            turno.reservar(paciente)
            messages.success(request, 'Turno agendado con éxito.')
            return redirect('turnero_reservar')  # Redirigir a la misma página sin filtros
        except ValidationError as e:
            error_message = str(e)
    
    # Contexto para la renderización
    context = {
        'turnos': turnos_disponibles,
        'medicos': medicos,
        'especialidades': especialidades,
        'pacientes': pacientes,
        'selected_especialidad': selected_especialidad,
        'selected_medico': selected_medico,
        'selected_date': selected_date,
        'error': locals().get('error_message', None),  # Mensaje de error si existe
    }
    
    return render(request, 'gestion_turnos/turnero_reservar.html', context)



@login_required
def turnero_cancelar(request, turno_id=None):

    medicos = Medico.objects.all().order_by('apellido', 'nombre')
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')

    # Obtener filtros de la URL
    selected_paciente = request.GET.get('paciente')
    selected_medico = request.GET.get('medico')
    selected_date = request.GET.get('fecha')

    query = {
        'paciente_id': selected_paciente,
        'medico_id': selected_medico,
        'fecha': selected_date
    }

    # Filtrar turnos ocupados
    turnos_ocupados = Turno.objects.filter(estado='ocupado')
    turnos_ocupados = filtrar_turnos(turnos_ocupados, query)

    if request.method == 'POST' and turno_id:
        turno = get_object_or_404(Turno, id=turno_id)

        try:
            turno.cancelar()
            messages.success(request, 'Turno cancelado con éxito!')
            return redirect('turnero_cancelar')  # Asegúrate de que redirijas correctamente
        except ValidationError as e:
            messages.error(request, str(e))

    context = {
        'turnos': turnos_ocupados,
        'pacientes': pacientes,
        'medicos': medicos,
        'selected_paciente': selected_paciente,
        'selected_medico': selected_medico,
        'selected_date': selected_date,
        'error': locals().get('error_message', None),  # Mensaje de error si existe
    }
    return render(request, 'gestion_turnos/turnero_cancelar.html', context)


@login_required
def turnero_bloquear(request):
    return render(request, 'gestion_turnos/turnero_bloquear.html')

@login_required
def dar_presente(request):
    return render(request, 'gestion_turnos/dar_presente.html')

@login_required
def sala_espera(request):
    return render(request, 'gestion_turnos/sala_espera.html')