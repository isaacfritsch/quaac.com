from functools import wraps
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from espaco.models import Espaco
from questoes.models import Questao

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

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        
        espaco_id = request.GET.get("espaco") or request.POST.get("espaco") or kwargs.get('espaco')

        # Obter o objeto Espaco
        if espaco_id:
            espaco = get_object_or_404(Espaco, id=espaco_id)
        else:
            return HttpResponseForbidden("Comunidade não encontrada ou não especificada.")
        
       
        if espaco.user != request.user:
            return HttpResponseForbidden("Você não tem permissão para acessar este recurso.")        
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view



