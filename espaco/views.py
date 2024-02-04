from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from urllib.parse import unquote
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Espaco, Tag
from .forms import CreateSpaceForm, CreateTagForm
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView

# Create your views here.

def test_view(request): 
    
    return render(request, 'espaco/home.html')

def espaco_list_view(request):   
    
    espacos = Espaco.objects.all()
    
    context = {
        'espacos': espacos,
    }
    
    return render(request, 'espaco/lista_espaco.html', context)


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
    espaco_solicitado = get_object_or_404(Espaco, slug=slug)
    
    # Verifica se o espaço atual é diferente do solicitado
    if 'current_espaco' in request.session:
        espaco_atual = request.session['current_espaco']
        if espaco_atual != espaco_solicitado.id:
            # Se o espaço mudou, redefine selected_tags
            request.session['selected_tags'] = []
    else:
        espaco_atual = None    
    
    if 'selected_tags' in request.session:
        selected_tags = request.session['selected_tags']
    else:
        selected_tags = []

    if None in selected_tags:
        selected_tags.remove(None)
        
    request.session['current_espaco'] = espaco_solicitado.id
    request.session['selected_tags'] = selected_tags
    context = {
        'espaco':espaco_solicitado,        
        'selected_tags': selected_tags,        
    }

    return render(request, 'espaco/space.html', context)

def lista_tags(request):
    
    espaco = request.GET.get("espaco")
    categoria = request.GET.get("categoria")
    
    espaco_desejado = Espaco.objects.get(id=espaco)
    
    if categoria == 'all':
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id).values_list('name', flat=True)        
    else:
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria).values_list('name', flat=True) 
    context = {
        'nomes_tags': sorted(nomes_tags)
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

def tag_creation(request, espaco):
    
    espaco_desejado = Espaco.objects.get(id=espaco)    
    
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = CreateTagForm(request.POST)        
                
        
        error_messages = form.errors                 
        
        # check whether it's valid:
        if form.is_valid():
            nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=form.instance.category).values_list('name', flat=True)
        
            if form.instance.name in nomes_tags:            
                form.add_error('name', 'Esta tag já existe nesta categoria. Escolha outro nome.')
                error_messages = form.errors
                return render(request, 'espaco/tag_modal.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })
            form.instance.space = espaco_desejado
            form.instance.user = request.user
            tag_instance = form.save(commit=False)
            tag_instance.save()
            
            response = HttpResponse(status=204, headers={'HX-Trigger': 'taglistchanged'})            
            return response
        
        return render(request, 'espaco/tag_modal.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })

    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = CreateTagForm()        
         
    
    return render(request, 'espaco/tag_modal.html', {'form': form,                                                     
                                                     'espaco_desejado': espaco_desejado,})   

def search_tag(request):
    search_text = request.POST.get("search")
    
    espaco = request.POST.get("espaco")
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, name__icontains=search_text).values_list('name', flat=True)
    
    context = {'results': results}
    
    return render(request, 'espaco/tag_search.html', context)


def search_category(request):
    
    search_text = request.POST.get("category")
    
    espaco = request.POST.get("espaco")  
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, category__icontains=search_text).values_list('category', flat=True)
    
    results = sorted(set(results)) 
    
    context = {'results': results, "search_text" : search_text}
    
    return render(request, 'espaco/category_search.html', context)


def processar_categoria(request):
    if request.method == 'POST':
        categoria = request.POST.get("category")        
        return HttpResponse((
    f'<input class="input is-link" id="modal-tag-category-form" readonly '
    f'type="text" '
    f'placeholder="Selecione ou crie uma categoria" '
    f'name="category" '
    f'value="{categoria}" '
    f'hx-post="{{% url \'search_category\' %}}" '
    f'hx-target=\'#category_selection\' '
    f'hx-vals=\'{{"espaco": {{"{{espaco_desejado.id}}"}}}}\' '
    f'hx-headers=\'{{"X-CSRFToken": "{{ csrf_token }}"}}\' '
    f'hx-trigger="keyup changed delay:500ms"> '   
    
))
        
        
def search_space(request):
    search_text = request.POST.get("search")
    
    results = Espaco.objects.filter(
    Q(title__icontains=search_text) | Q(description__icontains=search_text)
)
    
    context = {'results': results}
    
    return render(request, 'espaco/space_search.html', context)


def lista_categorias(request):

    espaco = request.GET.get("espaco") 

    espaco_solicitado = Espaco.objects.get(id=espaco)

    quantidade_tags_por_categoria = Tag.objects.filter(space=espaco_solicitado).values('category').annotate(quantidade_tags=Count('id')).order_by('category')

    quantidade_total_tags = Tag.objects.filter(space=espaco_solicitado).aggregate(quantidade_total=Count('id'))['quantidade_total']

    context = {
        'espaco':espaco_solicitado,
        'quantidade_tags_por_categoria':quantidade_tags_por_categoria,        
        'quantidade_total_tags': quantidade_total_tags,
    }

    return render(request, 'espaco/lista_categorias.html', context)






