
from django.urls import path
from espaco import views



urlpatterns = [
    path('', views.test_view, name='home'),
    path('espaco/lista_tags/', views.lista_tags, name='lista_tags'),
    path('create_space/', views.create_space, name='create_space'),
    path('redirect_to_space/', views.redirect_to_space, name='redirect_to_space'),
    path('espaco_list_view/', views.espaco_list_view, name='espaco_list_view'),
    path('espaco/<slug:slug>/', views.url_espaco, name='url_espaco'),    
    path('processar_tags/<str:tag>/', views.processar_tags, name='processar_tags'),
    path('tag_creation/<str:espaco>/', views.tag_creation, name='tag_creation'),
    path('search_tag/', views.search_tag, name='search_tag'), 
    path('search_category/', views.search_category, name='search_category'),
    path('search_space/', views.search_space, name='search_space'),
    path('processar_categoria/', views.processar_categoria, name='processar_categoria'), 
    path('lista_categorias/', views.lista_categorias, name='lista_categorias'),
    path('botao_edicao_tag/', views.botao_edicao_tag, name='botao_edicao_tag'),
    path('botao_tag_confirmar_deletar/', views.botao_tag_confirmar_deletar, name='botao_tag_confirmar_deletar'),
        
]