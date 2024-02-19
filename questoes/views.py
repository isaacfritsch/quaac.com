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
from django.contrib.auth.decorators import login_required
from espaco.models import Espaco, Tag
from .forms import QuestaoForm, AlternativaForm
from espaco.forms import CreateSpaceForm, TagForm
from questoes.models import Questao, Alternativa
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from django.core.paginator import Paginator

def question_create(request, espaco):

    espaco_desejado = Espaco.objects.get(title=espaco)
    
    request.session['selected_tags_questoes'] = []

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = QuestaoForm(request.POST)        
                
        
        error_messages = form.errors                 
        
        # check whether it's valid:
        if form.is_valid():
            nomes_tags = Tag.objects.filter(space=espaco_desejado.id).values_list('name', flat=True)
        
            if form.instance.name in nomes_tags:            
                form.add_error('name', 'Essa tag já existe. Escolha outro nome.')
                error_messages = form.errors
                return render(request, 'questoes/create_question.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })
            form.instance.space = espaco_desejado
            form.instance.user = request.user
            tag_instance = form.save(commit=False)
            tag_instance.save()
            
            response = HttpResponse(status=204)            
            return response
        
        return render(request, 'questoes/create_question.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })

    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = QuestaoForm()        


    return render(request, 'questoes/create_question.html', {'form': form,                                                     
                                                     'espaco': espaco_desejado,})
    
def tag_creation2(request, espaco):
    
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
                return render(request, 'questoes/tag_modal2.html', {'form': form, 
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
        
        return render(request, 'questoes/tag_modal2.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado,                                                                                                                  
                                                         })

    # if a GET (or any other method) we'll create a blank form
    else:
        
        form = TagForm()        
         
    
    return render(request, 'questoes/tag_modal2.html', {'form': form,                                                     
                                                     'espaco_desejado': espaco_desejado,})
    
def search_category2(request):
    
    search_text = request.POST.get("category")
    
    espaco = request.POST.get("espaco")  
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, category__icontains=search_text).values_list('category', flat=True)
    
    results = sorted(set(results)) 
    
    context = {'results': results, "search_text" : search_text}
    
    return render(request, 'questoes/category_search2.html', context)


def processar_categoria2(request):
    if request.method == 'POST':
        categoria = request.POST.get("category")        
        return HttpResponse((
    f'<input class="input is-primary" id="modal-tag-category-form2" readonly '
    f'type="text" '
    f'placeholder="Selecione ou crie uma categoria" '
    f'name="category" '
    f'value="{categoria}" '
    f'hx-post="{{% url \'search_category2\' %}}" '
    f'hx-target=\'#category_selection2\' '
    f'hx-vals=\'{{"espaco": {{"{{espaco_desejado.id}}"}}}}\' '
    f'hx-headers=\'{{"X-CSRFToken": "{{ csrf_token }}"}}\' '
    f'hx-trigger="keyup changed delay:500ms"> '
))
        
def search_tag2(request):
    search_text = request.POST.get("search")
    
    espaco = request.POST.get("espaco")
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, name__icontains=search_text).values_list('name', flat=True)
    
    context = {'results': results}
    
    return render(request, 'questoes/tag_search2.html', context)

def processar_tags2(request, tag):

    selected_tags = request.session['selected_tags_questoes']
    #caso de criar tag
    if tag in selected_tags:
        selected_tags.remove(tag)
    else:
        selected_tags.append(tag)


    

    tag_obj = Tag.objects.get(name=tag)      
    espaco = tag_obj.space
    espaco_desejado = Espaco.objects.get(title=espaco.title)
    categoria = tag_obj.category


    request.session['selected_tags_questoes'] = selected_tags
    selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])


    

    # Add HX-Trigger to the response
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({"taglistchanged": json.dumps({"espaco": espaco_desejado.id, "categoria": categoria}),
                                        "eventupdateselectedtags": {"selected2_tags_json": selected2_tags_json}
                                                 })
    return response

def tag_edicao2(request):
    
    if request.method == 'GET':
                               
        tag = request.GET.get("tag")
        tag = Tag.objects.get(name=tag)      
        espaco = tag.space
        espaco_desejado = Espaco.objects.get(title=espaco.title)
    
    if request.method == 'POST':
        
        tag = request.POST.get("tag")
                           
        tag = Tag.objects.get(name=tag)
        
        tag_original = tag.name  
             
        espaco = tag.space        
        espaco_desejado = Espaco.objects.get(title=espaco.title)
        
        
        # create a form instance and populate it with data from the request:
        form = TagForm(request.POST, instance=tag)       
        
           
        
        nomes_tags = Tag.objects.filter(space = espaco_desejado.id).values_list('name', flat=True)


        if request.POST['name'] in nomes_tags:

            form.add_error('name', 'Essa tag já existe. Escolha outro nome.')            
            tag = Tag.objects.get(name=tag_original)
            return render(request, 'questoes/tag_modal_edit2.html', {'form': form,                                                         
                                                         'espaco_desejado': espaco_desejado,
                                                         'tag':tag,                                                                                                                                                                         
                                                         })

        # check whether it's valid:
        if form.is_valid():
            error_messages = form.errors
            form.instance.space = espaco_desejado
            form.instance.user = request.user
            tag_instance = form.save(commit=False)
            tag_instance.save()
            
            selected_tags = request.session['selected_tags_questoes']
            #caso de deletar tag
            for i in range(len(selected_tags)):
        
                if selected_tags[i] == tag_original:   
                    selected_tags[i] = form.instance.name
            

            request.session['selected_tags_questoes'] = selected_tags
            selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])
            
            response = HttpResponse(status=204)
            response["Hx-Trigger"] = json.dumps({"taglistchangededit": json.dumps({"espaco": espaco_desejado.id, "categoria": form.instance.category}),
                                                 "eventupdateselectedtags": {"selected2_tags_json": selected2_tags_json}
                                                 })
            return response


        error_messages = form.errors
        return render(request, 'questoes/tag_modal_edit2.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco_desejado': espaco_desejado, 
                                                         'tag': tag,                                                                                                                 
                                                         })
    else:
        
        form = TagForm(instance=tag)         
    
    return render(request, 'questoes/tag_modal_edit2.html', {'form': form,                                               
                                                     'espaco_desejado': espaco_desejado,
                                                     'tag': tag,})
    
def lista_categorias2(request):

    espaco = request.GET.get("espaco") 

    espaco_solicitado = Espaco.objects.get(id=espaco)

    quantidade_tags_por_categoria = Tag.objects.filter(space=espaco_solicitado).values('category').annotate(quantidade_tags=Count('id')).order_by('category')

    quantidade_total_tags = Tag.objects.filter(space=espaco_solicitado).aggregate(quantidade_total=Count('id'))['quantidade_total']

    context = {
        'espaco':espaco_solicitado,
        'quantidade_tags_por_categoria':quantidade_tags_por_categoria,        
        'quantidade_total_tags': quantidade_total_tags,
    }

    return render(request, 'questoes/lista_categorias2.html', context)

def lista_tags2(request):
    
    if request.GET.get("espaco"):
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
        return render(request, 'questoes/lista_tags2.html', context)
    else:
        total = request.GET.get("total")   
    
        total = ast.literal_eval(total)
        espaco = total["espaco"]
        categoria =  total["categoria"]
        
        espaco_desejado = Espaco.objects.get(id=espaco)
        nomes_tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria).values_list('name', flat=True) 
        context = {
            'nomes_tags': sorted(nomes_tags)
        }
        return render(request, 'questoes/lista_tags2.html', context)
    
def update_tags_selecionadas2(request):
    
    selected_tags = request.session['selected_tags_questoes'] 


    request.session['selected_tags_questoes'] = selected_tags

    response = render(request, 'questoes/tags_selecionadas2.html', {
         'selected_tags': selected_tags,
    })

    return response

def selecionar_desselecionar2(request, tag):

    selected_tags = request.session['selected_tags_questoes']
    #caso de criar tag
    if tag in selected_tags:
        selected_tags.remove(tag)
    else:
        selected_tags.append(tag)    

    tag_obj = Tag.objects.get(name=tag)      
    espaco = tag_obj.space
    espaco_desejado = Espaco.objects.get(title=espaco.title)
    categoria = tag_obj.category


    request.session['selected_tags_questoes'] = selected_tags
    selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])    

    # Add HX-Trigger to the response
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({"selecionardesselecionar": json.dumps({"espaco": espaco_desejado.id, "categoria": categoria}),
                                        "eventupdateselectedtags": {"selected2_tags_json": selected2_tags_json}
                                                 })
    return response


def botao_tag_confirmar_deletar2(request):
    if request.method == 'POST':
        tag_name = request.POST.get("tag")
        tag = Tag.objects.get(name=tag_name)
        tag.delete()

        selected_tags = request.session['selected_tags_questoes']
        #caso de deletar tag
        if tag_name in selected_tags:
            selected_tags.remove(tag_name)
            
        request.session['selected_tags_questoes'] = selected_tags
        selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])
        
              
        espaco = tag.space
        espaco_desejado = Espaco.objects.get(title=espaco.title)
        categoria = tag.category
        
        response = HttpResponse(status=204)
        response["Hx-Trigger"] = json.dumps({"taglistchangeddelete": json.dumps({"espaco": espaco_desejado.id, "categoria": categoria}),
                                                 "eventupdateselectedtags": {"selected2_tags_json": selected2_tags_json}
                                                 })
        return response
    
def create_alternativa(request):
    
    if request.method == 'GET':

        form = AlternativaForm()

        return render(request, 'questoes/create_alternativa.html', {'form': form})





    
    
    
