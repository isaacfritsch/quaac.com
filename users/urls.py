from django.urls import path
from .views import user_register, user_login, user_logout, refresh_navbar

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('refresh_navbar/', refresh_navbar, name='refresh_navbar'),
]