from typing import Any
import json
import ast
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from django.contrib.contenttypes.models import ContentType
from urllib.parse import unquote
from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.utils.crypto import get_random_string
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from espaco.models import Tag, Espaco
from .forms import QuestaoForm, CommentForm, SolucaoForm, ReplyForm, ReplysolucaoForm
from espaco.forms import CreateSpaceForm, TagForm
from questoes.models import Questao, Comment, Reply, Solucao, Replysolucao, Like, Resolucao
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from quaac.decorators import custom_login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden


    
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

def search_category2_edit(request):
    
    search_text = request.POST.get("category")
    
    espaco = request.POST.get("espaco")  
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, category__icontains=search_text).values_list('category', flat=True)
    
    results = sorted(set(results)) 
    
    context = {'results': results, "search_text" : search_text}
    
    return render(request, 'questoes/category_search2_edit.html', context)


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
        
def processar_categoria2_edit(request):
    if request.method == 'POST':
        categoria = request.POST.get("category")        
        return HttpResponse((
    f'<input class="input is-primary" id="modal-tag-category-form2_edit" readonly '
    f'type="text" '
    f'placeholder="Selecione ou crie uma categoria" '
    f'name="category" '
    f'value="{categoria}" '
    f'hx-post="{{% url \'search_category2_edit\' %}}" '
    f'hx-target=\'#category_selection2_edit\' '
    f'hx-vals=\'{{"espaco": {{"{{espaco_desejado.id}}"}}}}\' '
    f'hx-headers=\'{{"X-CSRFToken": "{{ csrf_token }}"}}\' '
    f'hx-trigger="keyup changed delay:500ms"> '
))
        
def search_tag2(request):
    search_text = request.POST.get("search")
    
    espaco = request.POST.get("espaco")
    
    espaco_desejado = Espaco.objects.get(id=espaco)
        
    results = Tag.objects.filter(space=espaco_desejado.id, name__icontains=search_text).values_list('name', flat=True)
    
    context = {'results': results, 'espaco': espaco_desejado}
    
    return render(request, 'questoes/tag_search2.html', context)

from django.http import HttpResponse
import json
from .models import Tag

def processar_tags2(request, tag):
    espaco_id = request.POST.get("espaco")
    selected_tags = request.session.get('selected_tags_questoes', [])

    def remover_tag_e_filhos(tag_obj, selected_tags):
        """
        Remove a tag e todos os seus filhos recursivamente da lista de tags selecionadas.
        """
        if tag_obj.name in selected_tags:
            selected_tags.remove(tag_obj.name)
        for filho in tag_obj.children.all():
            remover_tag_e_filhos(filho, selected_tags)

    # Busca a tag no banco de dados
    try:
        tag_obj = Tag.objects.get(space=espaco_id, name=tag)
        
        if tag in selected_tags:
            remover_tag_e_filhos(tag_obj, selected_tags)
        
        categoria = tag_obj.category

    except Tag.DoesNotExist:
        selected_tags = []
        categoria = ""

      
    # Atualiza a sessão com a lista de tags selecionadas
    request.session['selected_tags_questoes'] = selected_tags
    selected2_tags_json = json.dumps(selected_tags)
    
    # Cria a resposta com os gatilhos necessários
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({
        "taglistchanged": json.dumps({"espaco": espaco_id, "categoria": categoria}),
        "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
    })
    return response


def tag_edicao2(request):
    
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
            return render(request, 'questoes/tag_modal_edit2.html', {'form': form,                                                         
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
            
            selected_tags = request.session['selected_tags_questoes']
            #caso de deletar tag
            for i in range(len(selected_tags)):
        
                if selected_tags[i] == tag_original:   
                    selected_tags[i] = form.instance.name
            

            request.session['selected_tags_questoes'] = selected_tags
            selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])
            
            response = HttpResponse(status=204)
            response["Hx-Trigger"] = json.dumps({"taglistchangededit": json.dumps({"espaco": espaco_desejado.id, "categoria": form.instance.category}),
                                                 "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
                                                 })
            return response


        error_messages = form.errors
        return render(request, 'questoes/tag_modal_edit2.html', {'form': form, 
                                                         'error_messages': error_messages,
                                                         'espaco': espaco_desejado, 
                                                         'tag': tag,                                                                                                                 
                                                         })
    else:
        
        form = TagForm(instance=tag)         
    
    return render(request, 'questoes/tag_modal_edit2.html', {'form': form,                                               
                                                     'espaco': espaco_desejado,
                                                     'tag': tag,})
    
def lista_categorias2(request):

    espaco = request.GET.get("espaco") 

    espaco_solicitado = Espaco.objects.get(id=espaco)

    quantidade_tags_por_categoria = Tag.objects.filter(space=espaco_solicitado).values('category').annotate(quantidade_tags=Count('id')).order_by(Lower('category'))

    quantidade_total_tags = Tag.objects.filter(space=espaco_solicitado).aggregate(quantidade_total=Count('id'))['quantidade_total']

    context = {
        'espaco':espaco_solicitado,
        'quantidade_tags_por_categoria':quantidade_tags_por_categoria,        
        'quantidade_total_tags': quantidade_total_tags,
    }

    return render(request, 'questoes/lista_categorias2.html', context)

def tag_edicao_botao2(request):
    tag = request.POST.get('tag')
    
    espaco_id = request.POST.get('espaco')
    
    context = {
        'tag': tag,
        'espaco_id': espaco_id,
        'csrf_token': request.COOKIES.get('csrftoken')
    }
    
    button_html = render_to_string('questoes/tag_edicao_button2.html', context)
    return HttpResponse(button_html)

def lista_tags2(request):
    if request.GET.get("espaco"):
        espaco = request.GET.get("espaco")
        categoria = request.GET.get("categoria")

        espaco_desejado = Espaco.objects.get(id=espaco)
        
        tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria)

        tag_list = []
        for tag in tags:
            tag_list.append({
                "id": tag.id,
                "parent": tag.parent.id if tag.parent else "#",
                "text": tag.name,
            })

        context = {
            'tags': json.dumps(tag_list),
            'espaco': espaco_desejado,
            'selected_tags_questoes': json.dumps(request.session.get('selected_tags_questoes', []))  # Passar selected_tags para o template
        }
        return render(request, 'questoes/lista_tags2.html', context)
    else:
        total = request.GET.get("total")
        total = ast.literal_eval(total)
        espaco = total["espaco"]
        categoria = total["categoria"]

        espaco_desejado = Espaco.objects.get(id=espaco)
        
        
        tags = Tag.objects.filter(space=espaco_desejado.id, category=categoria)

        tag_list = []
        for tag in tags:
            tag_list.append({
                "id": tag.id,
                "parent": tag.parent.id if tag.parent else "#",
                "text": tag.name,
            })

        context = {
            'tags': json.dumps(tag_list),
            'espaco': espaco_desejado,
            'selected_tags_questoes': json.dumps(request.session.get('selected_tags_questoes', []))  # Passar selected_tags para o template
        }
        return render(request, 'questoes/lista_tags2.html', context)
    
def update_tags_selecionadas2(request):
    
    selected_tags = request.session['selected_tags_questoes'] 
    espaco_id = request.GET.get("espaco")
    espaco = Espaco.objects.get(id=espaco_id)

    request.session['selected_tags_questoes'] = selected_tags

    response = render(request, 'questoes/tags_selecionadas2.html', {
         'selected_tags': selected_tags,
         'espaco': espaco,
    })

    return response

def selecionar_desselecionar_lista2(request):
    
    espaco_id = request.POST.get("espaco")
    
    
    selected_tags_questoes = json.loads(request.POST.get("selected_tags_questoes"))        
    deselected_tags_questoes = json.loads(request.POST.get("deselected_tags_questoes"))    
    
    # Recuperar as tags selecionadas da sessão
    session_selected_tags = request.session.get('selected_tags_questoes', [])

    # Adicionar tags selecionadas que não estão na sessão
    for tag in selected_tags_questoes:
        if tag not in session_selected_tags:
            session_selected_tags.append(tag)

    # Remover tags deselecionadas que estão na sessão
    for tag in deselected_tags_questoes:
        if tag in session_selected_tags:
            session_selected_tags.remove(tag)

    # Atualizar a sessão
    request.session['selected_tags_questoes'] = session_selected_tags
    selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])
    
    # Assumindo que todas as tags têm a mesma categoria
    if session_selected_tags:
        tag_obj = Tag.objects.get(space=espaco_id, name=session_selected_tags[0])
        categoria = tag_obj.category
    else:
        categoria = None
    
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({
        "selecionardesselecionar": json.dumps({"espaco": espaco_id, "categoria": categoria}),
        "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
    })
    return response

def selecionar_desselecionar2(request, tag):
    espaco_id = request.POST.get("espaco")    
    selected_tags = request.session['selected_tags_questoes']
    #caso de criar tag
    if tag in selected_tags:
        selected_tags.remove(tag)
    else:
        selected_tags.append(tag)    
    
    tag_obj = Tag.objects.get(space=espaco_id, name=tag)

    categoria = tag_obj.category


    request.session['selected_tags_questoes'] = selected_tags
    selected2_tags_json = json.dumps(request.session['selected_tags_questoes'])    

    # Add HX-Trigger to the response
    response = HttpResponse(status=204)
    response["Hx-Trigger"] = json.dumps({"selecionardesselecionar": json.dumps({"espaco": espaco_id, "categoria": categoria}),
                                        "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
                                                 })
    return response


def botao_tag_confirmar_deletar2(request):
    if request.method == 'POST':
        tag_name = request.POST.get("tag")
        espaco_id = request.POST.get("espaco")

        tag = Tag.objects.get(space=espaco_id, name=tag_name)
        
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
                                                 "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
                                                 })
        return response
    
# def create_alternativa(request, espaco):
    
#     espaco_desejado = espaco.objects.get(title=espaco)    
    
#     if request.method == 'GET':
        
#         form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm, extra=1, max_num=10)
        
#         form_alternativa = form_alternativa_factory()        
        
#         form_number = request.GET.get("totalForms")
        
#         if form_number == None:
#             form_number = 0       
        
#         for form in form_alternativa:
#             form.prefix =  form.prefix.replace(form.prefix[-1], form_number)
        
#         return render(request, 'questoes/create_alternativa.html', {'form_alternativa': form_alternativa,                                                                                                                                                                                                                                                                                                                                                  
#                                                                     'espaco': espaco_desejado}) 
        
 
  
# def question_create(request, espaco):

#     espaco_desejado = espaco.objects.get(title=espaco)   
    
#     if request.method == 'POST': 
        
#         form_number = request.POST.get("totalForms")
        
#         data = {
#          "alternativa_set-TOTAL_FORMS": form_number,
#         "alternativa_set-INITIAL_FORMS": "0",
#         }
               
#         form_questao = QuestaoForm(request.POST)
        
#         form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm, max_num=10)
#         post_data = request.POST.copy()

#         # Update post_data with the contents of dict2
#         post_data.update(data)

#         # Convert post_data to a normal Python dictionary
#         post_dict = {key: value for key, value in post_data.items()}

#         # Now pass the combined dictionary to the form
        
#         form_alternativa = form_alternativa_factory(post_dict)
        
#         form_questao = QuestaoForm(request.POST)      
        
#         if request.session['selected_tags_questoes'] == []:
#             form_questao.add_error('tags', 'A questão precisa ter pelo menos uma tag selecionada')
                
#             return render(request, 'questoes/create_question_form.html', {'form_questao': form_questao,                                                                                                                
#                                                             'espaco': espaco_desejado,                                                                                                                  
#                                                             })                
        
#         if form_questao.is_valid() and form_alternativa.is_valid():

#             question = form_questao.save(commit=False)  # Create instance, don't save yet
            
#             question.user = request.user
#             question.space = espaco_desejado  # Assign the "espaco"
                  
#             question.save()  # Now save to the database 
#             question_obj = Questao.objects.get(id=question.id)  
#             form_alternativa.instance = question_obj
#             # for form in form_alternativa:
#             #     print(form.data)           
#             #     form.instance.question = question_obj
#             #     form.save() 
            
#             form_alternativa.save()
                        
#             tags = request.session['selected_tags_questoes']
            
#             for tag_name in tags:

#                 tag_obj = Tag.objects.get(name=tag_name, space=espaco_desejado.id)

#                 question_obj.tags.add(tag_obj)
             
#             response = HttpResponse(204)
            
#             response["Hx-Redirect"] = reverse('questao', kwargs={'question': question.id})
#             return response
            
           
#         return render(request, 'questoes/create_question_form.html', {'form_questao': form_questao,                                                                                                                                                                                                                                               
#                                                     'espaco': espaco_desejado,                                                                                                                  
#                                                         })
        
#     else:
        
#         form_questao = QuestaoForm()
        
#     request.session['selected_tags_questoes'] = []     


#     return render(request, 'questoes/create_question.html', {'form_questao': form_questao,                                                                                                                  
#                                                      'espaco': espaco_desejado,})  

# def question_create(request, espaco):
#     espaco_desejado = espaco.objects.get(title=espaco)   
    
#     if request.method == 'POST': 
#         form_questao = QuestaoForm(request.POST)

#         if request.session.get('selected_tags_questoes', []) == []:
#             form_questao.add_error('tags', 'A questão precisa ter pelo menos uma tag selecionada')
#             return render(request, 'questoes/create_question_form.html', {'form_questao': form_questao, 'espaco': espaco_desejado})                
        
#         if form_questao.is_valid():
#             question = form_questao.save(commit=False)
#             question.user = request.user
#             question.space = espaco_desejado
#             question.save()

#             tags = request.session['selected_tags_questoes']
#             for tag_name in tags:
#                 tag_obj = Tag.objects.get(name=tag_name, space=espaco_desejado.id)
#                 question.tags.add(tag_obj)
             
#             response = HttpResponse(204)
#             response["Hx-Redirect"] = reverse('questao', kwargs={'question': question.id})
#             return response

#         return render(request, 'questoes/create_question_form.html', {'form_questao': form_questao, 'espaco': espaco_desejado})
        
#     else:
#         form_questao = QuestaoForm()
#         form_solucao = SolucaoForm()
#         request.session['selected_tags_questoes'] = []     

#     return render(request, 'questoes/create_question.html', {'form_questao': form_questao, 'espaco': espaco_desejado, 'form_solucao': form_solucao})



@custom_login_required
def question_create(request, espaco):
    
    espaco_desejado = Espaco.objects.get(title=espaco)
        
    form_questao = QuestaoForm(request.POST or None)
    form_solucao = SolucaoForm(request.POST or None)

    if request.method == 'POST':       
        
        if form_questao.is_valid():
            tags = request.session.get('selected_tags_questoes', [])
            if tags == []:
                form_questao.add_error('tags', 'A questão precisa ter pelo menos uma tag selecionada')
                return render(request, 'questoes/create_question_form.html', {
                    'form_questao': form_questao, 'form_solucao': form_solucao, 'espaco': espaco_desejado
                })
            
            question = form_questao.save(commit=False)
            question.user = request.user
            question.space = espaco_desejado
            question.save()

            for tag_name in tags:
                tag_obj = Tag.objects.get(name=tag_name, space=espaco_desejado.id)
                question.tags.add(tag_obj)           
            
            if form_solucao.is_valid():
                bodysol = form_solucao.cleaned_data.get('bodysol', '').strip()
                if bodysol:  # Verifica se bodysol não está vazio
                    solution = form_solucao.save(commit=False)
                    solution.autor = request.user  # Associando o autor
                    solution.questao = question  # Associando a questão
                    solution.save()
                    
            if request.POST.get('action') == 'save_and_add_new':
                return render(request, 'questoes/create_question_form.html', {
                    'form_questao': QuestaoForm(), 'form_solucao': SolucaoForm(), 'espaco': espaco_desejado, 'questao_criada': True
                })            
            question_id = question.id
            
            request.session['questao_criada'] = True
            url = reverse('questao_criada', kwargs={'id': question_id})            
            response = HttpResponse()
            response["Hx-Redirect"] = url           
            return response
        else:
            return render(request, 'questoes/create_question_form.html', {
                'form_questao': form_questao, 'form_solucao': form_solucao, 'espaco': espaco_desejado
            })
    else:
        form_questao = QuestaoForm()
        form_solucao = SolucaoForm()
        request.session['selected_tags_questoes'] = []

    if 'redirecionar' in request.GET:
        return render(request, 'questoes/create_question.html', {
            'form_questao': form_questao, 'form_solucao': form_solucao, 'espaco': espaco_desejado
        })
    else:
        url = reverse('question_create', kwargs={'espaco': espaco_desejado.title}) + '?redirecionar=true'
        response = HttpResponse()
        response["Hx-Redirect"] = url           
        return response
    
def questao_criada(request, id):
    
    question = get_object_or_404(Questao, id=id)
    
    # Retrieve the variable from the session
    questao_criada = request.session.get('questao_criada', False)

    # Optionally, clear the variable from the session if it shouldn't persist
    if 'questao_criada' in request.session:
        del request.session['questao_criada']
    
    return render(request, 'questoes/questao_criada.html', {'question': question, 'questao_criada': questao_criada})

def questao(request, question):          
        
    question1 = Questao.objects.get(id=question)
    
    espaco_desejado = Espaco.objects.get(title=question1.space)
    
    tags = question1.tags.all()
    
    return render(request, 'questoes/questao.html', {'question': question1,                                                                                                                  
                                                     'espaco': espaco_desejado,
                                                     'tags': tags,                                                     
                                                    })
    
def comentario(request):
    
    question_id = request.GET.get("question")
    if not question_id:
       question_id = request.POST.get("question")     
    question = Questao.objects.get(id=question_id)    
    comentarios = question.comment_set.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.autor = request.user            
            comment.questao = question
            comment.save()
            trigger_events = {
            f"comentariosalvo_{question_id}": True, 
            f"atualizatabquestao_{question_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
        else:
            return HttpResponse()
    else:
        form = CommentForm()
        
    context = {
        'comentarios':comentarios,
        'question': question,        
        'form': form        
    }   

    return render(request, 'questoes/comentario.html', context)

def editar_comentario(request):
    
    comentario_id = request.GET.get("comentario")
    if not comentario_id:
       comentario_id = request.POST.get("comentario") 
    comentario = get_object_or_404(Comment, id=comentario_id)
    
    if comentario.autor != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este comentário.")
    
    if request.method == 'GET':
        
        form = CommentForm(instance=comentario)
        context = {
            'form': form,
            'comentario': comentario
        }
        return render(request, 'questoes/editar_comentario.html', context)
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            
            question_id = comentario.questao.id
            trigger_events = {
            f"comentariosalvo_{question_id}": True,            
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
        
def delete_comentario(request):
    comentario_id = request.POST.get("comentario")
    comentario = Comment.objects.get(id=comentario_id)
    question_id = comentario.questao.id
    if request.user == comentario.autor:
        if request.method == 'POST':
            comentario.delete()
            trigger_events = {
            f"comentariosalvo_{question_id}": True,
            f"atualizatabquestao_{question_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
        return HttpResponse()
    
def add_reply(request):
    
    comentario_id = request.GET.get("comentario")
    if not comentario_id:
       comentario_id = request.POST.get("comentario")     
    comentario = Comment.objects.get(id=comentario_id)    
    replys = comentario.replies.all()     
    
    if request.method == 'POST' and request.user.is_authenticated:
        formreply = ReplyForm(request.POST)
        if formreply.is_valid():
            reply = formreply.save(commit=False)
            reply.autor = request.user            
            reply.comment = comentario
            reply.save()
            
            trigger_events = {
            f"replysalvo_{comentario_id}": True,
            f"atualizatabcomentario_{comentario_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
        else:
            return HttpResponse()
    else:
        formreply = ReplyForm()
        
    context = {
        'replys':replys,
        'comentario': comentario,        
        'formreply': formreply        
    }   

    return render(request, 'questoes/reply.html', context)

def editar_reply(request):

    reply_id = request.GET.get("reply")
    if not reply_id:
       reply_id = request.POST.get("reply")
    reply = Reply.objects.get(id=reply_id)
    
    if reply.autor != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este comentário.")
    
    if request.method == 'GET':
        
        form = ReplyForm(instance=reply)
        context = {
            'form': form,
            'reply': reply
        }
        return render(request, 'questoes/editar_reply.html', context)
    
    if request.method == 'POST':
        
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            
            comentario_id = reply.comment.id
            trigger_events = {
            f"replysalvo_{comentario_id}": True,            
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})

def delete_reply(request):
    reply_id = request.POST.get("reply")
    reply = Reply.objects.get(id=reply_id)
    
    if request.user == reply.autor:
        if request.method == 'POST':
            reply.delete()
            comentario_id = reply.comment.id
            trigger_events = {
            f"replysalvo_{comentario_id}": True,
            f"atualizatabcomentario_{comentario_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
        return HttpResponse()
    

        
def solucao(request):
    
    question_id = request.GET.get("question")
    if not question_id:
       question_id = request.POST.get("question")     
    question = Questao.objects.get(id=question_id)    
    solucoes = question.solucao_set.all()   
    
    if request.method == 'POST' and request.user.is_authenticated:
        formsolucao = SolucaoForm(request.POST)
        if formsolucao.is_valid():
            solucao = formsolucao.save(commit=False)
            solucao.autor = request.user            
            solucao.questao = question
            solucao.save()            
            
            trigger_events = {
            f"solucaosalvo_{question_id}": True,
            f"atualizatabquestao_{question_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
        else:
            return HttpResponse()
    else:
        formsolucao = SolucaoForm()
        
    context = {
        'solucoes':solucoes,
        'question': question,        
        'formsolucao': formsolucao       
    }   

    return render(request, 'questoes/solucao.html', context)

def delete_solucao(request):
    solucao_id = request.POST.get("solucao")
    solucao = Solucao.objects.get(id=solucao_id)
    
    question_id = solucao.questao.id
    if request.user == solucao.autor:
        if request.method == 'POST':
            solucao.delete()
            trigger_events = {
            f"solucaosalvo_{question_id}": True,
            f"atualizatabquestao_{question_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})            
        return HttpResponse()

def add_reply_solucao(request):

    solucao_id = request.GET.get("solucao")
    if not solucao_id:
       solucao_id = request.POST.get("solucao")     
    solucao = Solucao.objects.get(id=solucao_id)    
    replys_solucao = solucao.replies_solucao.all()   
    
    if request.method == 'POST' and request.user.is_authenticated:
        formreplysolucao = ReplysolucaoForm(request.POST)
        if formreplysolucao.is_valid():
            reply_solucao = formreplysolucao.save(commit=False)
            reply_solucao.autor = request.user            
            reply_solucao.solucao = solucao
            reply_solucao.save()
            
            trigger_events = {
            f"replysolucaosalvo_{solucao_id}": True,
            f"atualizatabsolucao_{solucao_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})        
            
        else:
            return HttpResponse()
    else:
        formreplysolucao = ReplysolucaoForm()        
        
    context = {
        'replys_solucao':replys_solucao,
        'solucao': solucao,        
        'formreply': formreplysolucao        
    }   

    return render(request, 'questoes/reply_solucao.html', context)

def delete_reply_solucao(request):
    reply_id = request.POST.get("replysolucao")
    reply = Replysolucao.objects.get(id=reply_id)
    
    if request.user == reply.autor:
        if request.method == 'POST':
            reply.delete()
            solucao_id = reply.solucao.id
            trigger_events = {
            f"replysolucaosalvo_{solucao_id}": True,
            f"atualizatabsolucao_{solucao_id}": True
            }
            
            trigger_events_json = json.dumps(trigger_events)
           
            return HttpResponse(status=204, headers={'HX-Trigger': trigger_events_json})
            
            
        return HttpResponse()

def like_question(request):
    question_id = request.POST.get("question")
    question = Questao.objects.get(id=question_id) 
    
    content_type = ContentType.objects.get_for_model(question)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=question.id,
    )
    if not created:
        # If like already exists, remove it
        like.delete()
           
    return HttpResponse(status=204, headers={'HX-Trigger': f"atualizatabquestao_{question_id}"})
    

def questao_int_tab(request):
    question_id = request.GET.get("question")
         
    question = Questao.objects.get(id=question_id)
    
    context = {
        'question': question
    }
    
    return render(request, 'questoes/questao_int_tab.html', context)

def like_comment(request):
    comentario_id = request.POST.get("comentario")
    comentario = Comment.objects.get(id=comentario_id) 
    
    content_type = ContentType.objects.get_for_model(comentario)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=comentario.id,
    )
    if not created:
        # If like already exists, remove it
        like.delete()
    
    return HttpResponse(status=204, headers={'HX-Trigger': f'atualizatabcomentario_{comentario_id}'})

def comment_tab(request):
    comentario_id = request.GET.get("comentario")
         
    comentario = Comment.objects.get(id=comentario_id)
    
    context = {
        'comentario': comentario
    }
    
    return render(request, 'questoes/comment_tab.html', context)

def like_reply(request):
    reply_id = request.POST.get("reply")
    reply = Reply.objects.get(id=reply_id) 
    
    content_type = ContentType.objects.get_for_model(reply)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=reply.id,
    )
    if not created:
        # If like already exists, remove it
        like.delete()
    
    return HttpResponse(status=204, headers={'HX-Trigger': f'atualizatabreply_{reply_id}'})

def reply_tab(request):
    reply_id = request.GET.get("reply")
         
    reply = Reply.objects.get(id=reply_id)
    
    context = {
        'reply': reply
    }
    
    return render(request, 'questoes/reply_tab.html', context)

def like_solucao(request):
    solucao_id = request.POST.get("solucao")
    solucao = Solucao.objects.get(id=solucao_id) 
    
    content_type = ContentType.objects.get_for_model(solucao)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=solucao.id,
    )
    if not created:
        # If like already exists, remove it
        like.delete()
    
    return HttpResponse(status=204, headers={'HX-Trigger': f'atualizatabsolucao_{solucao_id}'})

def solucao_tab(request):
    solucao_id = request.GET.get("solucao")
         
    solucao = Solucao.objects.get(id=solucao_id)
    
    context = {
        'solucao': solucao
    }
    
    return render(request, 'questoes/solucao_tab.html', context)

def like_reply_solucao(request):
    reply_id = request.POST.get("reply")
    reply = Replysolucao.objects.get(id=reply_id) 
    
    content_type = ContentType.objects.get_for_model(reply)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=reply.id,
    )
    if not created:        
        like.delete()          
    return HttpResponse(status=204, headers={'HX-Trigger': f'atualizatabsolucaoreply_{reply_id}'})

def reply_solucao_tab(request):
    reply_id = request.GET.get("reply")

    reply = Replysolucao.objects.get(id=reply_id)
    
    context = {
        'reply': reply
    }
    
    return render(request, 'questoes/reply_solucao_tab.html', context)

def marcar_resolvida(request):
    if request.method == "POST":
        questao_id = request.POST.get("question")    
        questao = Questao.objects.get(id=questao_id)
        
        resolucao, created = Resolucao.objects.get_or_create(
            user=request.user,
            questao=questao,
            defaults={'resolvida': True}
        )
        if created:
            questao.times_solved = questao.times_solved + 1
            resolucao.resolvida = True
            
            resolucao.save()
            questao.save()

        if not created and not resolucao.resolvida:            
            questao.times_solved = questao.times_solved +1
            resolucao.resolvida = True
            
            resolucao.save()
            questao.save()
            

        response = render(request, 'questoes/marcar_resolvida.html')
        response.status_code = 200
        return response
    else:
        return HttpResponse("Invalid request method", status=400)
    
def questoes_por_tag(request):    
    espaco_id = request.GET.get("espaco")  
    espaco = Espaco.objects.get(id=espaco_id)
    
    selected_tags = request.session.get('selected_tags', [])
    filter_nao_respondidas = request.GET.get("nao_respondidas") == 'true'
    filter_com_comentarios = request.GET.get("com_comentarios") == 'true'
    filter_com_resolucao = request.GET.get("com_resolucao") == 'true'
    
    page_num = request.GET.get("page")

    # Base queryset para todas as questões do espaço
    questoes = Questao.objects.filter(space=espaco)

    # Filtragem por tags
    if selected_tags:
        tags = Tag.objects.filter(name__in=selected_tags)
        questoes = questoes.filter(tags__in=tags).distinct()

    # Filtragem para questões não respondidas
    if filter_nao_respondidas:
        questoes = questoes.filter(
            Q(resolucao__resolvida=False) | 
            Q(resolucao__isnull=True)
        )

    # Filtragem para questões com comentários
    if filter_com_comentarios:
        questoes = questoes.annotate(comentario_count=Count('comment')).filter(comentario_count__gt=0)

    # Filtragem para questões com resolução
    if filter_com_resolucao:
        questoes = questoes.annotate(solucao_count=Count('solucao')).filter(solucao_count__gt=0)

    # Ordenação e paginação
    questoes = questoes.order_by('-id')
    paginator = Paginator(questoes, 5)  # Mostrar 5 questões por página
    page = paginator.get_page(page_num)

    context = {
        'espaco': espaco,
        'page': page,
        'tags': selected_tags,
        'respondidas': filter_nao_respondidas,
        'comentadas': filter_com_comentarios,
        'resolucao': filter_com_resolucao,
    }

    return render(request, 'questoes/questoes_filtradas.html', context)






    
    





    
    
    
