# turnos.views.liquidacion_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def liquidacion_honorarios(request):
    return render(request, 'liquidacion/liquidacion.html')