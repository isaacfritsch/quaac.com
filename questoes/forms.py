from django import forms
from .models import Questao, Alternativa



class QuestaoForm(forms.ModelForm):

    confirm = forms.BooleanField(
        required=True,  # Ensure the user checks it
        help_text="Please confirm that the question is not duplicated!"
    )

    class Meta:
        model = Questao
        fields = ['user', 'space', 'body', 'current_answer', 'times_solved', 'tags']
        widgets = {
        'user': forms.HiddenInput(),
        'space': forms.HiddenInput(),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user'].required = False
        self.fields['space'].required = False
        self.fields['confirm'].required = True
        self.fields['body'].required = True
        self.fields['current_answer'].required = False
        self.fields['times_solved'].required = False
        self.fields['tags'].required = True
        
class AlternativaForm(forms.ModelForm):   

    class Meta:
        model = Alternativa
        fields = ['question', 'text', 'correct']
        widgets = {
        'question': forms.HiddenInput(),        
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['question'].required = False
        self.fields['text'].required = True
        self.fields['correct'].required = True
        