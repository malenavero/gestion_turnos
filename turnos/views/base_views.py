# turnos.views.base_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def panel_principal(request):
    return render(request, 'main.html')
