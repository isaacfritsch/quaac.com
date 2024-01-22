from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomAuthenticationForm(forms.Form):
    
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
       label="Password",
       strip=False,
       widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
   )
    error_messages = {
        "invalid_login": 
            "Por favor, informe um email e(ou) senha corretos. Note que ambos "
            "os campos são case-sensitive."
        ,
        "inactive": "Esta conta está inativa.",
    }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')   
    
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255, validators=[User.alphanumeric_validator], required=True)
    
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user