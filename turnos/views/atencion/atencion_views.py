# turnos/views/atencion/atencion_views.py

from datetime import date
from django.forms import ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from turnos.models import Especialidad, Medico, Paciente, Turno
from turnos.models.historia_clinica import EntradaHistoria, HistoriaClinica
from turnos.utils import filtrar_turnos



@login_required
def atencion(request):
    return render(request, 'atencion/atencion.html')


@login_required
def atencion_sala_espera(request, turno_id=None, accion=None):
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
    turnos_en_espera = Turno.objects.filter(estado='acreditado', fecha_hora__date=today)
    turnos_en_espera = filtrar_turnos(turnos_en_espera, query)

    if request.method == 'POST' and turno_id:
        turno = get_object_or_404(Turno, id=turno_id)
        pacienteId = turno.paciente.id

        try:
            if accion == 'llamar':
                messages.info(request, f"Llamando nuevamente al paciente {turno.paciente.nombre} {turno.paciente.apellido}")
            elif accion == 'ausente':
                turno.marcar_ausente()
                messages.success(request, 'Turno marcado como ausente.')
                return redirect('atencion_sala_espera')
            elif accion == 'atender':
                turno.atender()
                url = reverse('atencion_historia_clinica_detail', args=[pacienteId])
                return HttpResponseRedirect(f"{url}?turno_id={turno_id}")        
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


@login_required
def atencion_historia_clinica(request):
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
    pacientes_lista = pacientes
    selected_paciente = request.GET.get('paciente')

    if selected_paciente:
        pacientes_lista = pacientes.filter(id=selected_paciente)
    

    context = {
        'pacientes': pacientes,
        'pacientes_lista': pacientes_lista,
        'selected_paciente': selected_paciente,
    }
    return render(request, 'atencion/atencion_historia_clinica.html', context)

@login_required
def atencion_historia_clinica_detail(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historia_clinica, _ = HistoriaClinica.objects.get_or_create(paciente=paciente)
    turno_asociado = request.GET.get('turno_id')

    if request.method == 'POST':
        diagnostico = request.POST.get('diagnostico')
        tratamiento = request.POST.get('tratamiento')
        receta = request.POST.get('receta', '')
        notas_adicionales = request.POST.get('notas_adicionales', '')

        # Obtenemos el medico del user
        medico = Medico.objects.filter(email=request.user.email).first()
        
        # Crea la entrada de historia clínica y asocia el médico y su especialidad
        EntradaHistoria.objects.create(
            historia_clinica=historia_clinica,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            receta=receta,
            notas_adicionales=notas_adicionales,
            medico=medico,
        )
        
        if(turno_asociado):
            turno = get_object_or_404(Turno, id=turno_asociado)
            turno.atendido()
            messages.success(request, 'HC actualizada. Siguientes pacientes:')
            return redirect('atencion_sala_espera')

        
        messages.success(request, 'Nueva entrada agregada exitosamente.')
        return redirect('atencion_historia_clinica_detail', paciente_id=paciente_id)

    # Ordenar las entradas de la historia clínica de más nueva a más vieja
    entradas_ordenadas = historia_clinica.entradas.all().order_by('-fecha')  

    context = {
        'paciente': paciente,
        'historia_clinica': historia_clinica,
        'entradas_ordenadas': entradas_ordenadas,
    }
    return render(request, 'atencion/atencion_historia_clinica_detail.html', context)


