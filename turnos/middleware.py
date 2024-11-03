from django.urls import reverse


class PreviousUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Llamar a la respuesta sin procesar la vista (esto permite usar process_view más adelante)
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Obtener el nombre de la vista actual usando `view_func` en `process_view`
        current_view = view_func.__name__

               # Definir la URL anterior según las reglas específicas, usando `reverse`
        if current_view in ["dar_presente", "turnero"]:
            request.session['previous_url'] = reverse('recepcion')
        
        elif current_view in ["turnero_bloquear", "turnero_cancelar", "turnero_reservar"]:
            request.session['previous_url'] = reverse('turnero')

        elif current_view in ["lista_pacientes", "lista_especialidades", "lista_medicos"]:
            request.session['previous_url'] = reverse('fabrica')
            
        elif current_view in ["atencion_historia_clinica_detail"]:
            request.session['previous_url'] = reverse('atencion_historia_clinica')

        elif current_view in ["recepcion", "atencion", "liquidacion_honorarios", "fabrica"]:
            request.session['previous_url'] = reverse('main')
        # Si no coincide con ninguna vista específica, no modifica `previous_url`

        return None
