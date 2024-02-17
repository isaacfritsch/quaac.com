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
from .forms import QuestaoForm
from questoes.models import Questao, Alternativa
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from django.core.paginator import Paginator

def question_create(request, espaco):

    espaco_desejado = Espaco.objects.get(title=espaco)

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

    
    
    
