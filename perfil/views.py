from django.shortcuts import render
from django.core.paginator import Paginator
from questoes.models import Questao, Comment, Reply, Solucao, Replysolucao, Like, Resolucao
from espaco.models import Tag, Espaco
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

def perfil(request):
    user = request.user
    context = {
        'user':user
    }
    return render(request, 'perfil/perfil.html', context)

def questoes_respondidas(request):
    user_id = request.GET.get("user")
    
    if user_id:
        # Filtrar questões resolvidas pelo usuário e ordenar do mais recente para o mais antigo
        resolucoes = Resolucao.objects.filter(user_id=user_id, resolvida=True).order_by('-resolved_at')
        questoes = Questao.objects.filter(resolucao__in=resolucoes).distinct().order_by('-resolucao__resolved_at')
    else:
        questoes = Questao.objects.none()
        
    respondidas = questoes.count()
    

    page_num = request.GET.get("page")
    paginator = Paginator(questoes, 5)  # Mostrar 5 questões por página
    page = paginator.get_page(page_num)

    context = {        
        'page': page,
        'user': user_id,
        'respondidas': respondidas,     
    }

    return render(request, 'perfil/questoes_respondidas.html', context)

def questoes_like(request):
    user_id = request.GET.get("user")

    if user_id:
        # Obter o ContentType para o modelo Questao
        questao_content_type = ContentType.objects.get_for_model(Questao)
        # Filtrar likes do usuário para o modelo Questao
        likes = Like.objects.filter(user_id=user_id, content_type=questao_content_type).order_by('-liked_at')
        # Obter as questões que o usuário deu like
        questoes = Questao.objects.filter(id__in=likes.values_list('object_id', flat=True)).distinct()
    else:
        questoes = Questao.objects.none()

    likes = questoes.count()
    page_num = request.GET.get("page")
    paginator = Paginator(questoes, 5)  # Mostrar 5 questões por página
    page = paginator.get_page(page_num)

    context = {        
        'page': page,
        'user': user_id,
        'likes':likes,       
    }

    return render(request, 'perfil/questoes_like.html', context)

def questoes_comentarios_resolucoes(request):
    user_id = request.GET.get("user")

    if user_id:
        # Filtrar comentários do usuário
        comentarios = Comment.objects.filter(autor_id=user_id).values_list('questao_id', flat=True)
        # Filtrar soluções do usuário
        solucoes = Solucao.objects.filter(autor_id=user_id).values_list('questao_id', flat=True)
        # Filtrar replies do usuário em comentários
        replies_comentarios = Reply.objects.filter(autor_id=user_id).values_list('comment__questao_id', flat=True)
        # Filtrar replies do usuário em soluções
        replies_solucoes = Replysolucao.objects.filter(autor_id=user_id).values_list('solucao__questao_id', flat=True)

        # Combinar todos os IDs de questões
        questao_ids = set(comentarios) | set(solucoes) | set(replies_comentarios) | set(replies_solucoes)
        
        # Filtrar questões com base nos IDs coletados
        questoes = Questao.objects.filter(id__in=questao_ids).distinct().order_by('-id')
    else:
        questoes = Questao.objects.none()
        
    questoes_comentarios = questoes.count()

    page_num = request.GET.get("page")
    paginator = Paginator(questoes, 5)  # Mostrar 5 questões por página
    page = paginator.get_page(page_num)

    context = {        
        'page': page,
        'user': user_id,
        'questoes_comentarios': questoes_comentarios,     
    }

    return render(request, 'perfil/questoes_comentarios_resolucoes.html', context)

def questoes_criadas(request):
    user_id = request.GET.get("user")

    if user_id:
        # Filtrar questões criadas pelo usuário e ordenar do mais recente para o mais antigo
        questoes = Questao.objects.filter(user_id=user_id).order_by('-id')
    else:
        questoes = Questao.objects.none()
        
    criadas = questoes.count()

    page_num = request.GET.get("page")
    paginator = Paginator(questoes, 5)  # Mostrar 5 questões por página
    page = paginator.get_page(page_num)

    context = {        
        'page': page,
        'user': user_id,
        'criadas': criadas,       
    }

    return render(request, 'perfil/questoes_criadas.html', context)

def comunidades_criadas(request):
    user_id = request.GET.get("user")
    
    if user_id:
        # Filtrar espaços criados pelo usuário e ordenar do mais recente para o mais antigo
        espacos = Espaco.objects.filter(user_id=user_id).order_by('-id')
    else:
        espacos = Espaco.objects.none()
    
    comunidades = espacos.count()
    context = {        
        'espacos': espacos,
        'user': user_id,
        'comunidades': comunidades,      
    }

    return render(request, 'perfil/comunidades_criadas.html', context)

def search_comunidade_perfil(request):
    search_text = request.POST.get("search")
    user_id = request.POST.get("user")
    
    if user_id and search_text:
        # Filtrar espaços pelo texto de pesquisa e pelo usuário criador
        results = Espaco.objects.filter(
            Q(user_id=user_id) & (Q(title__icontains=search_text) | Q(description__icontains=search_text))
        )
    else:
        results = Espaco.objects.none()

    context = {'results': results}
    
    return render(request, 'perfil/comunidade_search.html', context)

def informacoes_pessoais(request):
    
    return render(request, 'perfil/informacoes_pessoais.html')