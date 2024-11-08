   
# turnos/urls.py
from django.urls import path
from .views.base_views import panel_principal
from .views.fabrica.fabrica_views import fabrica
from .views.fabrica.fabrica_views import  *
from .views.recepcion.recepcion_views import *

from .views.atencion.atencion_views import atencion, atencion_sala_espera, atencion_historia_clinica, atencion_historia_clinica_detail
from .views.liquidacion.liquidacion_views import liquidacion_honorarios, generar_pdf

urlpatterns = [
    path('main/', panel_principal, name='main'),

    # fabrica
    path('fabrica/', fabrica, name='fabrica'),  

    path('especialidades/<int:pk>/ver/', ver_especialidad, name='ver_especialidad'),
    path('crear-especialidad/', crear_especialidad, name='crear_especialidad'),
    path('especialidades/', lista_especialidades, name='lista_especialidades'),
    path('especialidades/<int:pk>/editar/', editar_especialidad, name='editar_especialidad'),
    path('especialidades/eliminar/<int:pk>/', eliminar_especialidad, name='eliminar_especialidad'),

    path('medicos/<int:pk>/ver/', ver_medico, name='ver_medico'),
    path('crear-medico/', crear_medico, name='crear_medico'),
    path('medicos/', lista_medicos, name='lista_medicos'),
    path('medicos/<int:pk>/editar/', editar_medico, name='editar_medico'),
    path('medicos/eliminar/<int:pk>/', eliminar_medico, name='eliminar_medico'),

    path('pacientes/<int:pk>/ver/', ver_paciente, name='ver_paciente'),
    path('crear-paciente/', crear_paciente, name='crear_paciente'),
    path('pacientes/', lista_pacientes, name='lista_pacientes'),
    path('pacientes/<int:pk>/editar/', editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:pk>/', eliminar_paciente, name='eliminar_paciente'),



    #recepcion
    path('recepcion/', recepcion, name='recepcion'),

    path('turnero/', turnero, name='turnero'),
    path('turnero_reservar/', turnero_reservar, name='turnero_reservar'),
    path('turnero_reservar/<int:turno_id>/', turnero_reservar, name='turnero_reservar'),
    path('turnero_cancelar/', turnero_cancelar, name='turnero_cancelar'),
    path('turnero_cancelar/<int:turno_id>/', turnero_cancelar, name='turnero_cancelar'),
    path('turnero_bloquear/', turnero_bloquear, name='turnero_bloquear'),
    path('turnero_bloquear/<int:turno_id>/', turnero_bloquear, name='turnero_bloquear'),
       
    path('dar_presente/', dar_presente, name='dar_presente'),
    path('dar_presente/<int:turno_id>/', dar_presente, name='dar_presente'),
    path('api/paciente/<int:turno_id>/', obtener_datos_paciente, name='obtener_datos_paciente'),
    path('obras-sociales/<int:obra_social_id>/planes/', obtener_planes, name='obtener_planes'),
    
    #atencion
    path('atencion/', atencion, name='atencion'),
    path('atencion_sala_espera/', atencion_sala_espera, name='atencion_sala_espera'),
    path('atencion_sala_espera/<int:turno_id>/<str:accion>', atencion_sala_espera, name='atencion_sala_espera'),

    path('atencion_historia_clinica/', atencion_historia_clinica, name='atencion_historia_clinica'),
    path('atencion_historia_clinica/<int:paciente_id>/', atencion_historia_clinica_detail, name='atencion_historia_clinica_detail'),

    
    #liquidacion
    path('liquidacion/', liquidacion_honorarios, name='liquidacion_honorarios'),
    path('liquidacion/generar', liquidacion_honorarios, name='generar_pdf'),
    path('liquidacion/pdf/<int:medico_id>/', generar_pdf, name='generar_pdf'),
]
