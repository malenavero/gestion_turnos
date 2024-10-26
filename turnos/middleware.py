# middleware.py
class PreviousUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Guardar la URL anterior en la sesión
        if 'previous_url' not in request.session:
            request.session['previous_url'] = request.META.get('HTTP_REFERER')
        
        response = self.get_response(request)
        return response
