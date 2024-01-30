from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Espaco, Tag
from .forms import CreateSpaceForm
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView

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
    quantidade_tags_por_categoria = Tag.objects.filter(space=espaco).values('category').annotate(quantidade_tags=Count('id'))
    quantidade_total_tags = Tag.objects.filter(space=espaco).aggregate(quantidade_total=Count('id'))['quantidade_total']
    if 'selected_tags' in request.session:
        selected_tags = request.session['selected_tags']
    else:
        selected_tags = []  
        
    if None in selected_tags:
        selected_tags.remove(None)
        
    request.session['selected_tags'] = selected_tags 
    context = {
        'espaco':espaco,
        'quantidade_tags_por_categoria':quantidade_tags_por_categoria,
        'selected_tags': selected_tags,
        'quantidade_total_tags': quantidade_total_tags,
    }

    return render(request, 'espaco/space.html', context)

def lista_tags(request, espaco, categoria):
    espaco_desejado = Espaco.objects.get(title=espaco)
    if categoria == 'all':
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id).values_list('name', flat=True)
    else:
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria).values_list('name', flat=True)
        
    context = {
        'nomes_tags': list(nomes_tags)
    }
    
    return render(request, 'espaco/lista_tags.html', context)


def processar_tags(request, tag):   
    
    selected_tags = request.session['selected_tags']
    

    if tag not in selected_tags:
        selected_tags.append(tag)        
    else:
        selected_tags.remove(tag)
        
    if None in selected_tags:
        selected_tags.remove(None)
        
    request.session['selected_tags'] = selected_tags
    
    return render(request, 'espaco/tags_selecionadas.html', {'selected_tags': selected_tags})







