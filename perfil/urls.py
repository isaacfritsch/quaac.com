from django.urls import path
from perfil import views



urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('questoes_respondidas/', views.questoes_respondidas, name='questoes_respondidas'),
    path('questoes_like/', views.questoes_like, name='questoes_like'),
    path('questoes_comentarios_resolucoes/', views.questoes_comentarios_resolucoes, name='questoes_comentarios_resolucoes'),
    path('questoes_criadas/', views.questoes_criadas, name='questoes_criadas'),
    path('comunidades_criadas/', views.comunidades_criadas, name='comunidades_criadas'),
    path('search_comunidade_perfil/', views.search_comunidade_perfil, name='search_comunidade_perfil'),
    path('informacoes_pessoais/', views.informacoes_pessoais, name='informacoes_pessoais'),
]