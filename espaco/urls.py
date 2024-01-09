
from django.urls import path
from espaco import views

urlpatterns = [    
    path('', views.test_view),
]