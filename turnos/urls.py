   
# turnos/urls.py
from django.urls import path
from .views.base_views import panel_principal
from .views.fabrica.fabrica_views import fabrica, crear_especialidad, crear_paciente, crear_medico
from .views.gestion_turnos.gestion_turnos_views import gestion_turnos
from .views.atencion.atencion_views import atencion
from .views.liquidacion.liquidacion_views import liquidacion_honorarios

urlpatterns = [
    path('main/', panel_principal, name='main'),

    # fabrica
    path('fabrica/', fabrica, name='fabrica'),  
    path('crear-especialidad/', crear_especialidad, name='crear_especialidad'),
    path('crear-paciente/', crear_paciente, name='crear_paciente'),
    path('crear-medico/', crear_medico, name='crear_medico'),

    #gestion_turnos
    path('gestion-turnos/', gestion_turnos, name='gestion_turnos'),
    
    #atencion
    path('atencion/', atencion, name='atencion'),
    
    #liquidacion
    path('liquidacion/', liquidacion_honorarios, name='liquidacion')
]
