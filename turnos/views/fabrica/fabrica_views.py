# turnos.views.fabrica_views.py

from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from turnos.forms.fabrica.forms import EspecialidadForm, PacienteForm, MedicoForm
from turnos.models import Especialidad, Medico, Paciente, Turno
from django.contrib import messages
from turnos.decorators import group_required

@group_required("Jefatura Recepcion", "Recepcionistas")
def fabrica(request):
    return render(request, 'fabrica/fabrica.html')

@group_required("Jefatura Recepcion", "Recepcionistas")
def ver_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    return render(request, 'fabrica/ver_especialidad.html', {'especialidad': especialidad})

@group_required("Jefatura Recepcion")
def crear_especialidad(request):
    if request.method == "POST":
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad creada con éxito.')
            return redirect('lista_especialidades')
    else:
        form = EspecialidadForm()
    return render(request, 'fabrica/crear_especialidad.html', {'form': form})

@group_required("Jefatura Recepcion", "Recepcionistas")
def lista_especialidades(request):
    especialidades = Especialidad.objects.all().order_by('nombre')

    return render(request, 'fabrica/lista_especialidades.html', {
        'especialidades': especialidades
    })

@group_required("Jefatura Recepcion")
def editar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad modificada con éxito.')
            return redirect('lista_especialidades')
    else:
        form = EspecialidadForm(instance=especialidad)

    return render(request, 'fabrica/editar_especialidad.html', {'form': form})

@group_required("Jefatura Recepcion")
def eliminar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)

    if request.method == "POST":
        try:
            especialidad.delete()
            messages.success(request, 'Especialidad eliminada con éxito.')
            return redirect('lista_especialidades')
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'fabrica/lista_especialidades.html', {
                'especialidades': Especialidad.objects.all().order_by('nombre'),
            })



@group_required("Jefatura Recepcion", "Recepcionistas")
def ver_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'fabrica/ver_paciente.html', {'paciente': paciente})

@group_required("Jefatura Recepcion", "Recepcionistas")
def crear_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado con éxito.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'fabrica/crear_paciente.html', {'form': form})

@group_required("Jefatura Recepcion", "Recepcionistas")
def lista_pacientes(request):
    query = request.GET.get('query', '') 
    # Filtra los pacientes por nombre o apellido
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
    if query:
        pacientes = pacientes.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query)
        )

    context = {
        'pacientes': pacientes,
        'error_message': None if pacientes.exists() else 'No hay pacientes disponibles.'
    }
    return render(request, 'fabrica/lista_pacientes.html', context)

@group_required("Jefatura Recepcion", "Recepcionistas")
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente modificado con éxito.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'fabrica/editar_paciente.html', {'form': form})

@group_required("Jefatura Recepcion", "Recepcionistas")
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":    
        try:
            paciente.delete()
            messages.success(request, 'Paciente eliminado con éxito.')
            return redirect('lista_pacientes')
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'fabrica/lista_pacientes.html', {
                'pacientes': Paciente.objects.all().order_by('apellido', 'nombre')
            })


@group_required("Jefatura Recepcion", "Recepcionistas")
def ver_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'fabrica/ver_medico.html', {'medico': medico})

@group_required("Jefatura Recepcion")
def crear_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medico creado con éxito.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm()
    return render(request, 'fabrica/crear_medico.html', {'form': form})

@group_required("Jefatura Recepcion", "Recepcionistas")
def lista_medicos(request):
    especialidades = Especialidad.objects.all()
    selected_especialidad = request.GET.get('especialidad')

    if selected_especialidad:
        medicos = Medico.objects.filter(especialidad__id=selected_especialidad).order_by('apellido', 'nombre')
    else:
        medicos = Medico.objects.all().order_by('apellido', 'nombre')

    return render(request, 'fabrica/lista_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades,
        'selected_especialidad': selected_especialidad
    })

@group_required("Jefatura Recepcion")
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    disable_especialidad = Turno.objects.filter(medico=medico).exclude(estado='disponible').exists()
    
    if request.method == 'POST':
        # Si `disable_especialidad` es True, agrega la data a la request
        post_data = request.POST.copy()
        if disable_especialidad:
            post_data['especialidad'] = medico.especialidad_id
        form = MedicoForm(post_data, instance=medico, disable_especialidad=disable_especialidad)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Medico modificado con éxito.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm(instance=medico, disable_especialidad=disable_especialidad)

    return render(request, 'fabrica/editar_medico.html', {
        'form': form,
        'disable_especialidad': disable_especialidad,
    })

@group_required("Jefatura Recepcion")
def eliminar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == "POST":
        try:
            medico.delete()
            messages.success(request, 'Medico eliminado con éxito.')
            return redirect('lista_medicos')        
        except ValidationError as e:
            messages.error(request,  str(e))
            return render(request, 'fabrica/lista_medicos.html', {
                'medicos': Medico.objects.all().order_by('apellido', 'nombre')
            })





