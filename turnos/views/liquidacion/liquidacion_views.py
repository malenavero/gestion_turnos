# turnos.views.liquidacion_views.py

from django.utils import timezone
from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from weasyprint import HTML

from turnos.models import  Medico
from turnos.utils import get_month_name


@login_required
def liquidacion_honorarios(request):
    # Contenido de filtros
    medicos = Medico.objects.all().order_by('apellido', 'nombre')
    current_mes = timezone.localtime().month
    current_año = timezone.localtime().year
    meses = list(range(1, 13))
    años = list(range(2020, current_año +1))

    if request.GET:

        # Obtener los valores seleccionados desde el request
        selected_mes = request.GET.get('mes')
        selected_mes = int(selected_mes) if selected_mes else current_mes
        selected_año = request.GET.get('año')
        selected_medico = request.GET.get('medico')
        # Si no hay mes o año seleccionado, usa el mes y año actuales
        if not selected_mes or not selected_año:
            selected_mes = current_mes
            selected_año = current_año

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
            'meses': meses,
            'años': años,
        }
        return render(request, 'liquidacion/liquidacion_honorarios.html', context)
    
    context = {
        'medicos_selector': medicos,
        'meses': meses,
        'años': años,
    }

    return render(request, 'liquidacion/liquidacion_honorarios.html', context)

@login_required
def generar_pdf(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    total_honorarios, atendidos, ausentes = medico.calcular_honorarios()

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