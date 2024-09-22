# turnos.views.fabrica_views.py

from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from turnos.forms.fabrica.forms import EspecialidadForm, PacienteForm, MedicoForm
from turnos.models.especialidad import Especialidad

@login_required
def fabrica(request):
    return render(request, 'fabrica/fabrica.html')

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
def crear_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fabrica')
    else:
        form = MedicoForm()
    return render(request, 'fabrica/crear_medico.html', {'form': form})