
from django.urls import path
from espaco import views



urlpatterns = [
    path('', views.test_view, name='home'),
    path('create_space/', views.create_space, name='create_space'),
    path('espaco/<slug:slug>/', views.url_espaco, name='url_espaco'),
    path('espaco/lista_tags/<slug:espaco>/<slug:categoria>/', views.lista_tags, name='lista_tags'),
    path('processar_tags/<slug:tag>', views.processar_tags, name='processar_tags'),    
]