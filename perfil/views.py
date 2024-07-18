from django.shortcuts import render
from django.core.paginator import Paginator
from questoes.models import Questao, Comment, Reply, Solucao, Replysolucao, Like, Resolucao
from espaco.models import Tag, Espaco
from users.models import User

def perfil(request):    
    return render(request, 'perfil/perfil.html')

def pag_questoes_criadas(request):
    espaco_id = request.GET.get("espaco")
    user = request.GET.get("user")
    espaco = Espaco.objects.get(id=espaco_id) 
    
    page_num = request.GET.get("page")
    
    questoes = Questao.objects.filter(space=espaco,user=user)

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
    
