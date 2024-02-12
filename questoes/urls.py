from django.urls import path
from questoes import views



urlpatterns = [
    path('question_create/<str:espaco>', views.question_create, name='question_create'),         
]