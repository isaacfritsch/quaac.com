from typing import Any
import json
import ast
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse, QueryDict
from django.forms import formset_factory
from urllib.parse import unquote
from django.db.models import Count, Q
from django.utils.crypto import get_random_string
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from espaco.models import Espaco, Tag
from .forms import QuestaoForm, CommentForm, SolucaoForm, ReplyForm
from espaco.forms import CreateSpaceForm, TagForm
from questoes.models import Questao, Comment, Reply
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from django.core.paginator import Paginator


    
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
                                        "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
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
                                                 "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
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
                                        "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
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
                                                 "eventupdateselectedtags2": {"selected2_tags_json": selected2_tags_json}
                                                 })
        return response
    
# def create_alternativa(request, espaco):
    
#     espaco_desejado = Espaco.objects.get(title=espaco)    
    
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

#     espaco_desejado = Espaco.objects.get(title=espaco)   
    
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
#     espaco_desejado = Espaco.objects.get(title=espaco)   
    
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

from django.http import HttpResponse
from django.urls import reverse

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
                solution = form_solucao.save(commit=False)
                solution.autor = request.user # Associando o autor
                solution.questao = question # Associando a questão
                solution.save()
                
            response = HttpResponse(204)
            response["Hx-Redirect"] = reverse('questao', kwargs={'question': question.id})
            return response
        
        else:
            return render(request, 'questoes/create_question_form.html', {
                'form_questao': form_questao, 'form_solucao': form_solucao, 'espaco': espaco_desejado
            })
    
    else:
        form_questao = QuestaoForm()
        form_solucao = SolucaoForm()
        request.session['selected_tags_questoes'] = []     

    return render(request, 'questoes/create_question.html', {
        'form_questao': form_questao, 'form_solucao': form_solucao, 'espaco': espaco_desejado
    })
    
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
            return HttpResponse(status=204, headers={'HX-Trigger': 'comentariosalvo'})
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


def delete_comentario(request):
    comentario_id = request.POST.get("comentario")
    comentario = Comment.objects.get(id=comentario_id)
    
    if request.user == comentario.autor:
        if request.method == 'POST':
            comentario.delete()
            return HttpResponse(status=204, headers={'HX-Trigger': 'comentariosalvo'})
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
            return HttpResponse(status=204, headers={'HX-Trigger': 'replysalvo'})
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

def delete_reply(request):
    reply_id = request.POST.get("reply")
    reply = Reply.objects.get(id=reply_id)
    
    if request.user == reply.autor:
        if request.method == 'POST':
            reply.delete()
            return HttpResponse(status=204, headers={'HX-Trigger': 'replysalvo'})
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
            return HttpResponse(status=204, headers={'HX-Trigger': 'solucaosalvo'})
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






    
    





    
    
    
