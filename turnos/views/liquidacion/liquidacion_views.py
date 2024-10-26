# turnos.views.liquidacion_views.py

from django.utils import timezone
from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from weasyprint import HTML

from turnos.models import  Medico
from turnos.utils import get_month_name

CURRENT_MES = timezone.localtime().month
CURRENT_AÑO = timezone.localtime().year

MESES = list(range(1, 13))
AÑOS = list(range(2020, CURRENT_AÑO +1))

selected_mes = None
selected_año = None
selected_medico = None

@login_required
def liquidacion_honorarios(request):
    # Contenido de filtros
    medicos = Medico.objects.all().order_by('apellido', 'nombre')

    if request.GET:
        # Obtener los valores seleccionados desde el request
        selected_mes = request.GET.get('mes')
        selected_mes = int(selected_mes) if selected_mes else CURRENT_MES
        selected_año = request.GET.get('año')
        selected_medico = request.GET.get('medico')
        # Si no hay mes o año seleccionado, usa el mes y año actuales
        if not selected_mes or not selected_año:
            selected_mes = CURRENT_MES
            selected_año = CURRENT_AÑO

        selected_mes_name = get_month_name(selected_mes)
        # Listado de médicos a mostrar
        medicos_listado = medicos
        selected_medico = request.GET.get('medico')
        if selected_medico:
            medicos_listado = Medico.objects.filter(id=selected_medico)

        honorarios_data = []

        # Generar data
        for medico in medicos_listado:
            total_honorarios, atendidos, ausentes = medico.calcular_honorarios(mes=selected_mes, año=selected_año)

            if total_honorarios > 0:
                honorarios_data.append({
                    'medico': medico,
                    'total_honorarios': total_honorarios,
                    'turnos_atendidos': atendidos,
                    'turnos_ausentes_acreditados': ausentes
                })


        context = {
            'honorarios_data': honorarios_data,
            'medicos_selector': medicos,
            'selected_mes': selected_mes,
            'selected_mes_name': selected_mes_name,
            'selected_año': selected_año,
            'meses': MESES,
            'años': AÑOS,
        }
        return render(request, 'liquidacion/liquidacion_honorarios.html', context)
    
    context = {
        'medicos_selector': medicos,
         'meses': MESES,
        'años': AÑOS,
    }

    return render(request, 'liquidacion/liquidacion_honorarios.html', context)

@login_required
def generar_pdf(request, medico_id):

    # Obtenemos los valores de mes y año de la solicitud GET
    selected_mes = int(request.GET.get('mes', CURRENT_MES))
    selected_año = int(request.GET.get('año', CURRENT_AÑO))

    medico = get_object_or_404(Medico, id=medico_id)
    total_honorarios, atendidos, ausentes = medico.calcular_honorarios(mes=selected_mes, año=selected_año)

    context = {
        'mes': 'Octubre',
        'año': 2024,
        'medico': medico,
        'turnos_atendidos': atendidos,
        'turnos_ausentes_acreditados': ausentes,
        'total_honorarios': total_honorarios,
    }

    # Renderiza el HTML del PDF
    html_string = render_to_string('liquidacion/liquidacion_pdf.html', context)

    # Crea una respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liquidacion_honorarios.pdf"'

    # Generar el PDF
    HTML(string=html_string).write_pdf(response)

    return response