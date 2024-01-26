
from django.urls import path
from espaco import views



urlpatterns = [    
    path('', views.test_view, name='home'),
    path('create_space/', views.create_space, name='create_space'),
    path('espaco/<slug:slug>/', views.url_espaco, name='url_espaco'),
]