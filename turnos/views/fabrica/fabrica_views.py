# turnos.views.fabrica_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from turnos.forms.fabrica.forms import EspecialidadForm, PacienteForm, MedicoForm

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