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
    path('questao/<str:question>/', views.questao, name='questao'),    
    path('comentario/', views.comentario, name='comentario'),
    path('delete_comentario/', views.delete_comentario, name='delete_comentario'),
    path('add_reply/', views.add_reply, name='add_reply'),
    path('delete_reply/', views.delete_reply, name='delete_reply'),
    path('solucao/', views.solucao, name='solucao'),
    path('delete_solucao/', views.delete_solucao, name='delete_solucao'),
    path('add_reply_solucao/', views.add_reply_solucao, name='add_reply_solucao'),
    path('delete_reply_solucao/', views.delete_reply_solucao, name='delete_reply_solucao'),
    path('like_question/', views.like_question, name='like_question'),
    path('questao_int_tab/', views.questao_int_tab, name='questao_int_tab'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('comment_tab/', views.comment_tab, name='comment_tab'),
    path('like_reply/', views.like_reply, name='like_reply'),
    path('reply_tab/', views.reply_tab, name='reply_tab'),
    path('like_solucao/', views.like_solucao, name='like_solucao'),
    path('solucao_tab/', views.solucao_tab, name='solucao_tab'),
    path('like_reply_solucao/', views.like_reply_solucao, name='like_reply_solucao'),
    path('reply_solucao_tab/', views.reply_solucao_tab, name='reply_solucao_tab'),
    path('marcar_resolvida/', views.marcar_resolvida, name='marcar_resolvida'),        
]