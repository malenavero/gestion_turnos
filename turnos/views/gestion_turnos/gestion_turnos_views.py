# turnos.views.gestion_turnos_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def gestion_turnos(request):
    return render(request, 'gestion_turnos/gestion_turnos.html')