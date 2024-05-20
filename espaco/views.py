from typing import Any
import json
import ast
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from urllib.parse import unquote
from django.db.models import Count, Q
from django.urls import reverse
from questoes.models import Questao
from django.contrib.auth.decorators import login_required
from .models import Espaco, Tag
from .forms import CreateSpaceForm, TagForm
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from django.core.paginator import Paginator


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
    
def redirect_to_space(request):
    
    espaco = request.GET.get("espaco")
    espaco = Espaco.objects.get(id=espaco)
    slug_do_novo_espaco = espaco.slug
    response = HttpResponse()
    response["Hx-Redirect"] = reverse('url_espaco', kwargs={'slug': slug_do_novo_espaco})
    return response


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
    selected_tags_json = json.dumps(request.session['selected_tags'])    
    
    context = {
        'espaco':espaco_solicitado,        
        'selected_tags': selected_tags, 
        'selected_tags_json': selected_tags_json,
    }

    return render(request, 'espaco/space.html', context)

def lista_tags(request):
    
    if request.GET.get("espaco"):
        espaco = request.GET.get("espaco")
        categoria = request.GET.get("categoria")

        espaco_desejado = Espaco.objects.get(id=espaco)

        if categoria == 'all':
            nomes_tags = Tag.objects.filter(space=espaco_desejado.id).values_list('name', flat=True)        
        else:
            nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria).values_list('name', flat=True) 
        context = {
            'nomes_tags': sorted(nomes_tags),
            'espaco':espaco_desejado
        }
        return render(request, 'espaco/lista_tags.html', context)
    else:
        total = request.GET.get("total")   
    
        total = ast.literal_eval(total)
        espaco = total["espaco"]
        categoria =  total["categoria"]
        
        espaco_desejado = Espaco.objects.get(id=espaco)
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria).values_list('name', flat=True) 
        context = {
            'nomes_tags': sorted(nomes_tags),
            'espaco':espaco_desejado
        }
        return render(request, 'espaco/lista_tags.html', context)
    
def selecionar_desselecionar(request, tag):
    espaco_id = request.POST.get("espaco")
       
    selected_tags = request.session['selected_tags']
    #caso de criar tag
    if tag in selected_tags:
        selected_tags.remove(tag)
    else:
        selected_tags.append(tag)    
    
    tag_obj = Tag.objects.get(space=espaco_id, name=tag)
    
    categoria = tag_obj.category


    request.session['selected_tags'] = selected_tags
    selected_tags_json = json.dumps(request.session['selected_tags'])    

    # Add HX-Trigger to the response
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({"selecionardesselecionar": json.dumps({"espaco": espaco_id, "categoria": categoria}),
                                        "eventupdateselectedtags": {"selected_tags_json": selected_tags_json}
                                                 })
    return response

def processar_tags(request, tag):
    espaco_id = request.POST.get("espaco")
    selected_tags = request.session['selected_tags']
    #caso de criar tag
    if tag in selected_tags:
        selected_tags.remove(tag)
    else:
        selected_tags.append(tag)
    

    tag_obj = Tag.objects.get(space=espaco_id, name=tag)      
    
    categoria = tag_obj.category


    request.session['selected_tags'] = selected_tags
    selected_tags_json = json.dumps(request.session['selected_tags'])
    

    # Add HX-Trigger to the response
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({"taglistchanged": json.dumps({"espaco": espaco_id, "categoria": categoria}),
                                        "eventupdateselectedtags": {"selected_tags_json": selected_tags_json}
                                                 })
    return response

def tag_creation(request, espaco):
    
    espaco_desejado = Espaco.objects.get(id=espaco)    
    
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = TagForm(request.POST)        
                
        
        error_messages = form.errors                 
        
        # check whether it's valid:
        if form.is_valid():
            nomes_tags = Tag.objects.filter(space=espaco_desejado.id).values_list('name', flat=True)
        
            if form.instance.name in nomes_tags:            
                form.add_error('name', 'Essa tag já existe. Escolha outro nome.')
                error_messages = form.errors
                return render(request, 'espaco/tag_modal.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })
            form.instance.space = espaco_desejado
            form.instance.user = request.user
            tag_instance = form.save(commit=False)
            tag_instance.save()
            
            response = HttpResponse(status=204)
            response["Hx-Trigger"] = json.dumps({"taglistcreated": json.dumps({"espaco": espaco, "categoria": form.instance.category})})
            return response
        
        return render(request, 'espaco/tag_modal.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })

   
    else:
        
        form = TagForm()        
         
    
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

def search_category_edit(request):
    
    search_text = request.POST.get("category")
    
    espaco = request.POST.get("espaco")  
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, category__icontains=search_text).values_list('category', flat=True)
    
    results = sorted(set(results)) 
    
    context = {'results': results, "search_text" : search_text}
    
    return render(request, 'espaco/category_search_edit.html', context)


def processar_categoria(request):
    if request.method == 'POST':
        categoria = request.POST.get("category")        
        return HttpResponse((
    f'<input class="input is-primary" id="modal-tag-category-form" readonly '
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
        
def processar_categoria_edit(request):
    if request.method == 'POST':
        categoria = request.POST.get("category")        
        return HttpResponse((
    f'<input class="input is-primary" id="modal-tag-category-form_edit" readonly '
    f'type="text" '
    f'placeholder="Selecione ou crie uma categoria" '
    f'name="category" '
    f'value="{categoria}" '
    f'hx-post="{{% url \'search_category\' %}}" '
    f'hx-target=\'#category_selection_edit\' '
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

def tag_edicao(request):
    
    if request.method == 'GET':
                               
        tag = request.GET.get("tag")
        espaco_id = request.GET.get("espaco")
        tag = Tag.objects.get(space=espaco_id, name=tag)
        espaco_desejado = Espaco.objects.get(id=espaco_id)
    
    if request.method == 'POST':
        
        tag = request.POST.get("tag")
        espaco_id = request.POST.get("espaco")
        tag = Tag.objects.get(space=espaco_id, name=tag)
        tag_original = tag.name                
        espaco_desejado = Espaco.objects.get(id=espaco_id)
        
        
        # create a form instance and populate it with data from the request:
        form = TagForm(request.POST, instance=tag)           
        
        nomes_tags = Tag.objects.filter(space = espaco_desejado.id).values_list('name', flat=True)


        if request.POST['name'] in nomes_tags and request.POST['name'] != tag.name:

            form.add_error('name', 'Essa tag já existe. Escolha outro nome.')            
            tag = Tag.objects.get(name=tag_original)
            return render(request, 'espaco/tag_modal_edit.html', {'form': form,                                                         
                                                         'espaco': espaco_desejado,
                                                         'tag':tag,                                                                                                                                                                         
                                                         })

        # check whether it's valid:
        if form.is_valid():
            error_messages = form.errors
            form.instance.space = espaco_desejado
            form.instance.user = request.user
            tag_instance = form.save(commit=False)
            tag_instance.save()
            
            selected_tags = request.session['selected_tags']
            #caso de deletar tag
            for i in range(len(selected_tags)):
        
                if selected_tags[i] == tag_original:   
                    selected_tags[i] = form.instance.name
            

            request.session['selected_tags'] = selected_tags
            selected_tags_json = json.dumps(request.session['selected_tags'])
            
            response = HttpResponse(status=204)
            response["Hx-Trigger"] = json.dumps({"taglistchangededit": json.dumps({"espaco": espaco_desejado.id, "categoria": form.instance.category}),
                                                 "eventupdateselectedtags": {"selected_tags_json": selected_tags_json}
                                                 })
            return response


        error_messages = form.errors
        print(form.errors)
        return render(request, 'espaco/tag_modal_edit.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco': espaco_desejado, 
                                                         'tag': tag,                                                                                                                 
                                                         })
    else:
        
        form = TagForm(instance=tag)         
    
    return render(request, 'espaco/tag_modal_edit.html', {'form': form,                                               
                                                     'espaco': espaco_desejado,
                                                     'tag': tag,})

def botao_tag_confirmar_deletar(request):
    if request.method == 'POST':
        tag_name = request.POST.get("tag")
        espaco_id = request.POST.get("espaco")
        tag = Tag.objects.get(space=espaco_id, name=tag_name)
        tag.delete()

        selected_tags = request.session['selected_tags']
        #caso de deletar tag
        if tag_name in selected_tags:
            selected_tags.remove(tag_name)
            
        request.session['selected_tags'] = selected_tags
        selected_tags_json = json.dumps(request.session['selected_tags'])
        
              
        espaco = tag.space
        espaco_desejado = Espaco.objects.get(title=espaco.title)
        categoria = tag.category
        
        response = HttpResponse(status=204)
        response["Hx-Trigger"] = json.dumps({"taglistchangeddelete": json.dumps({"espaco": espaco_desejado.id, "categoria": categoria}),
                                                 "eventupdateselectedtags": {"selected_tags_json": selected_tags_json}
                                                 })
        return response



def update_tags_selecionadas(request):
    
    selected_tags = request.session['selected_tags'] 
    espaco_id = request.GET.get("espaco")
    espaco = Espaco.objects.get(id=espaco_id)

    request.session['selected_tags'] = selected_tags

    response = render(request, 'espaco/tags_selecionadas.html', {
         'selected_tags': selected_tags,
         'espaco': espaco,
    })

    return response

def ultimas_questoes_adicionadas(request):
    
    espaco = request.GET.get("espaco")
    page = request.GET.get("page")    
    
    espaco_desejado = Espaco.objects.get(id=espaco)
    question = Questao.objects.all().filter(space=espaco_desejado).order_by('-id')
    paginator = Paginator(question, 1)
    
    if not page:        
        page = 1
         
    else:        
        page = int(page)
        page += 1       
    try:
        question = paginator.page(page)
    except:
        return HttpResponse('')

    context = {
        'espaco': espaco_desejado,
        'questions' : question,
        'page' : page,
    }

    return render(request, 'espaco/ultimas_questoes_adicionadas.html', context)


    





