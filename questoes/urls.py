from django.urls import path
from questoes import views



urlpatterns = [
    path('question_create/<str:espaco>', views.question_create, name='question_create'),
    path('tag_creation2/<str:espaco>/', views.tag_creation2, name='tag_creation2'),
    path('search_category2/', views.search_category2, name='search_category2'),
    path('search_category2_edit/', views.search_category2_edit, name='search_category2_edit'),
    path('processar_categoria2/', views.processar_categoria2, name='processar_categoria2'),
    path('processar_categoria2_edit/', views.processar_categoria2_edit, name='processar_categoria2_edit'),
    path('search_tag2/', views.search_tag2, name='search_tag2'),
    path('processar_tags2/<str:tag>/', views.processar_tags2, name='processar_tags2'),
    path('tag_edicao2/', views.tag_edicao2, name='tag_edicao2'),
    path('lista_categorias2/', views.lista_categorias2, name='lista_categorias2'),
    path('espaco/lista_tags2/', views.lista_tags2, name='lista_tags2'),
    path('update_tags_selecionadas2/', views.update_tags_selecionadas2, name='update_tags_selecionadas2'),
    path('selecionar_desselecionar2/<str:tag>/', views.selecionar_desselecionar2, name='selecionar_desselecionar2'),
    path('botao_tag_confirmar_deletar2/', views.botao_tag_confirmar_deletar2, name='botao_tag_confirmar_deletar2'),
    path('create_alternativa/<str:espaco>/', views.create_alternativa, name='create_alternativa'),
    path('questao/<str:question>/', views.questao, name='questao'),            
]