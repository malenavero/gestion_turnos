# turnos.views.fabrica_views.py

from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from turnos.forms.fabrica.forms import EspecialidadForm, PacienteForm, MedicoForm
from turnos.models import Especialidad, Medico, Paciente
from turnos.models.turno import Turno

@login_required
def fabrica(request):
    return render(request, 'fabrica/fabrica.html')

@login_required
def ver_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    return render(request, 'fabrica/ver_especialidad.html', {'especialidad': especialidad})

@login_required
def crear_especialidad(request):
    if request.method == "POST":
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fabrica')
    else:
        form = EspecialidadForm()
    return render(request, 'fabrica/crear_especialidad.html', {'form': form})

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all().order_by('nombre')

    return render(request, 'fabrica/lista_especialidades.html', {
        'especialidades': especialidades
    })

@login_required
def editar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            return redirect('lista_especialidades')
    else:
        form = EspecialidadForm(instance=especialidad)

    return render(request, 'fabrica/editar_especialidad.html', {'form': form})

@login_required
def eliminar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)

    if request.method == "POST":
        try:
            especialidad.delete()
            return redirect('lista_especialidades')  # Cambia aquí
        except ValidationError as e:
            return render(request, 'fabrica/lista_especialidades.html', {
                'especialidades': Especialidad.objects.all().order_by('nombre'),
                'error_message': str(e)
            })

    return render(request, 'fabrica/confirmar_eliminacion_especialidad.html', {'especialidad': especialidad})


@login_required
def ver_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'fabrica/ver_paciente.html', {'paciente': paciente})

@login_required
def crear_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fabrica')
    else:
        form = PacienteForm()
    return render(request, 'fabrica/crear_paciente.html', {'form': form})

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'fabrica/lista_pacientes.html', {
        'pacientes': pacientes
    })

@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'fabrica/editar_paciente.html', {'form': form})

@login_required
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    try:
        paciente.delete()  # La validación ocurre en el método delete del modelo
    except ValidationError as e:
        return render(request, 'fabrica/lista_pacientes.html', {
            'pacientes': Paciente.objects.all().order_by('apellido', 'nombre'),
            'error_message': str(e)
        })

    return render(request, 'fabrica/confirmar_eliminacion_paciente.html', {'paciente': paciente})

@login_required
def ver_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'fabrica/ver_medico.html', {'medico': medico})

@login_required
def crear_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fabrica')
    else:
        form = MedicoForm()
    return render(request, 'fabrica/crear_medico.html', {'form': form})

@login_required
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

@login_required
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    form = MedicoForm(instance=medico)

    disable_especialidad = Turno.objects.filter(medico=medico).exclude(estado='disponible').exists()

    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('fabrica')

    return render(request, 'fabrica/editar_medico.html', {
        'form': form,
        'disable_especialidad': disable_especialidad,
    })


@login_required
def eliminar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    try:
            medico.delete()
    except ValidationError as e:
        return render(request, 'fabrica/lista_medicos.html', {
            'medicos': Medico.objects.all().order_by('apellido', 'nombre'),
            'error_message': str(e)
        })
    return render(request, 'fabrica/confirmar_eliminacion_medico.html', {'medico': medico})



