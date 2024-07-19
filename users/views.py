from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model


from django.http import HttpResponseRedirect, HttpResponse
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def user_register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()            
            password = form.cleaned_data.get('password1') 
            
            user = authenticate(request, email=email, password=password)
            
            # Log in the user
            login(request, user)
            
            # Redirect to a success page or homepage
            response = HttpResponse()
            response["Hx-Redirect"] = "/"
            return response
            
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomAuthenticationForm(request.POST)
        
        error_messages = form.error_messages
        
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Usuário autenticado com sucesso
                login(request, user)
                
                request.session['success_message'] = "Login bem-sucedido. Bem-vindo!"
                response = HttpResponse(status=204)
                response['HX-Trigger'] = 'userlogin'
                
                return response
                
            else:                
                # Usuário não autenticado - trate conforme necessário
                form.add_error(None, 'Credenciais inválidas. Verifique seu email e senha.')
        return render(request, 'registration/login.html', {'form': form, 'error_messages': error_messages})
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def useredit(request):
    if request.method == 'GET':
        user_email = request.GET.get("user")
        user = get_object_or_404(User, email=user_email)
        form = CustomUserChangeForm(instance=user)
        return render(request, 'perfil/user_modal_edit.html', {'form': form})
    
    elif request.method == 'POST':
        user_email = request.POST.get("user")
        user = get_object_or_404(User, email=user_email)       
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():            
            form.save()
            email = form.cleaned_data.get('email').lower()            
            password = form.cleaned_data.get('password1') 
            
            user = authenticate(request, email=email, password=password)
            
            login(request, user)
                        
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'useredited'
            
            return response

        
        return render(request, 'perfil/user_modal_edit.html', {'form': form})

    else:
        return HttpResponse(status=405)  # Method Not Allowed






       

    
