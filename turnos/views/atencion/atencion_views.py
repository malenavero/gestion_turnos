# turnos.views.atencion_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def atencion(request):
    return render(request, 'atencion/atencion.html')