
from django.urls import path
from espaco import views



urlpatterns = [
    path('', views.test_view, name='home'),
    path('espaco/lista_tags/', views.lista_tags, name='lista_tags'),
    path('create_space/', views.create_space, name='create_space'),
    path('espaco/<slug:slug>/', views.url_espaco, name='url_espaco'),    
    path('processar_tags/<str:tag>/', views.processar_tags, name='processar_tags'),
    path('tag_creation/<str:espaco>/', views.tag_creation, name='tag_creation'),
    path('search_tag/', views.search_tag, name='search_tag'),   
]