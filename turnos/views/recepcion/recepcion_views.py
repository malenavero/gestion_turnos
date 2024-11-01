# turnos.views.recepcion.recepcion_views.py

from django.forms import ValidationError
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from turnos.models import Especialidad, Medico, Paciente, Turno
from turnos.utils import filtrar_turnos

@login_required
def recepcion(request):
    return render(request, 'recepcion/recepcion.html')

@login_required
def turnero(request):
    return render(request, 'recepcion/turnero.html')

@login_required
def turnero_reservar(request, turno_id=None):
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

    if request.method == 'POST'and turno_id:
        paciente_id = request.POST.get('paciente_id')
        turno = get_object_or_404(Turno, id=turno_id)
        paciente = get_object_or_404(Paciente, id=paciente_id)

        try:
            turno.reservar(paciente)
            messages.success(request, 'Turno agendado con éxito.')
            return redirect('turnero_reservar')
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
    
    return render(request, 'recepcion/turnero_reservar.html', context)

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
            return redirect('turnero_cancelar')
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
    return render(request, 'recepcion/turnero_cancelar.html', context)

@login_required
def turnero_bloquear(request, turno_id=None):   
    medicos = Medico.objects.all().order_by('apellido', 'nombre')

    # Obtener filtros de la URL
    selected_medico = request.GET.get('medico')
    selected_date = request.GET.get('fecha')
    selected_estado = request.GET.get('estado')

    query = {
        'medico_id': selected_medico,
        'fecha': selected_date
    }


    # Filtrar turnos según estado
    if selected_estado == 'bloqueable':
        turnos_disponibles = Turno.objects.filter(estado='disponible')
    elif selected_estado == 'desbloqueable':
        turnos_disponibles = Turno.objects.filter(estado='bloqueado')
    else:
        # Si no hay estado seleccionado, traer tanto bloqueados como disponibles
        turnos_disponibles = Turno.objects.filter(estado__in=['disponible', 'bloqueado'])


    turnos_disponibles = filtrar_turnos(turnos_disponibles, query)

    if request.method == 'POST' and turno_id:
        turno = get_object_or_404(Turno, id=turno_id)

        try:
            if turno.estado == 'disponible':
                turno.bloquear()
                messages.success(request, 'Turno bloqueado con éxito!')
            elif turno.estado == 'bloqueado':
                turno.desbloquear()
                messages.success(request, 'Turno desbloqueado con éxito!')
            return redirect('turnero_bloquear')
        except ValidationError as e:
            messages.error(request, str(e))

    context = {
        'turnos': turnos_disponibles,
        'medicos': medicos,
        'selected_medico': selected_medico,
        'selected_date': selected_date,
        'selected_estado': selected_estado,
        'error': locals().get('error_message', None), 
    }
    return render(request, 'recepcion/turnero_bloquear.html', context)



@login_required
def dar_presente(request, turno_id=None):
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
    turnos_en_espera = Turno.objects.filter(estado='ocupado', fecha_hora__date=today)
    turnos_en_espera = filtrar_turnos(turnos_en_espera, query)

    if request.method == 'POST' and turno_id:
        turno = get_object_or_404(Turno, id=turno_id)
        # obtener el valor
        opcionPago = request.POST.get('opcionPago')
        try:
            if opcionPago == "particular":
                turno.cobrar("particular")
                turno.acreditar()
                messages.success(request, 'Cobro particular realizado con éxito. El paciente puede dirigirse a la sala de espera.')
            elif opcionPago == "obra-social":
                # Aquí podrías necesitar lógica adicional para manejar la obra social
                gestionar_acreditacion_obra_social(request, turno.paciente.id)
                messages.success(request, 'Acreditación de obra social realizada con éxito. El paciente puede dirigirse a la sala de espera.')

            return redirect('dar_presente')

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
    return render(request, 'recepcion/dar_presente.html', context)


@login_required
def gestionar_acreditacion_obra_social(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    
    if request.method == 'POST':
        paciente.obra_social = request.POST.get('obraSocial')
        paciente.credencial = request.POST.get('nroCredencial')
        paciente.plan = request.POST.get('plan')
        paciente.save()  # Guardar los cambios
        
