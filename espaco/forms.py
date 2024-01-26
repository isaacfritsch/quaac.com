from django import forms
from .models import Espaco

class CreateSpaceForm(forms.ModelForm):   
    
    class Meta:
        model = Espaco
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)