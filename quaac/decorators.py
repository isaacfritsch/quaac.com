from functools import wraps
from django.http import HttpResponse

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Dispara o evento HTMX
            response = HttpResponse(status=401)  # Status 401 para indicar que o usuário não está autenticado
            response['HX-Trigger'] = 'userloginrequired'
                     
            return response
        return view_func(request, *args, **kwargs)
    return _wrapped_view