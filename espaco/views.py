from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Espaco
from .forms import CreateSpaceForm

# Create your views here.

def test_view(request):
    return render(request, 'espaco/home.html')


def create_space(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            
            form = CreateSpaceForm(request.POST)
            if form.is_valid():
                novo_espaco = form.save(commit=False)
                novo_espaco.user = request.user  # Atribuir o usuário atual ao espaco
                novo_espaco.save()
                
                slug_do_novo_espaco = novo_espaco.slug
                
                response = HttpResponse()
                response["Hx-Redirect"] = reverse('url_espaco', kwargs={'slug': slug_do_novo_espaco})
                return response
        else:
            form = CreateSpaceForm()

        return render(request, 'espaco/create_space.html', {'form': form})
    
    else:
        return render(request, 'espaco/failure_create_space.html')


def url_espaco(request, slug):
    espaco = get_object_or_404(Espaco, slug=slug)
    return render(request, 'espaco/space.html', {'espaco': espaco})