from django.urls import path
from .views import user_register, user_login, user_logout, useredit, navbar
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),   
    path('useredit/', useredit, name='useredit'),
    path('navbar/', navbar, name='navbar'), 
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_complete"),
    
]