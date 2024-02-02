from django import forms
from .models import Espaco, Tag

class CreateSpaceForm(forms.ModelForm):   
    
    class Meta:
        model = Espaco
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class CreateTagForm(forms.ModelForm):   

    class Meta:
        model = Tag
        fields = ['name', 'category', 'space', 'user']
        widgets = {
        'user': forms.HiddenInput(),
        'space': forms.HiddenInput(),
        }    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['space'].required = False
        self.fields['user'].required = False
        
    
        