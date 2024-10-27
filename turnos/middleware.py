# middleware.py
class PreviousUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Guardar la URL anterior en la sesión solo si HTTP_REFERER está presente
        if 'HTTP_REFERER' in request.META:
            request.session['previous_url'] = request.META['HTTP_REFERER']
        
        response = self.get_response(request)
        return response

