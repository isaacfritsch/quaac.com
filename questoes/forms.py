from django import forms
from .models import Questao, Comment, Solucao, Reply
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField



class QuestaoForm(forms.ModelForm):

    confirm = forms.BooleanField(
        required=True,  # Ensure the user checks it
        help_text="Please confirm that the question is not duplicated!"
    )  

    class Meta:
        model = Questao
        fields = ['user', 'space', 'body', 'times_solved', 'tags', ]
        
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
        self.fields['times_solved'].required = False
        self.fields['tags'].required = False        
        
        self.fields['body'] = SummernoteTextFormField()
        
        
# class AlternativaForm(forms.ModelForm):   

#     class Meta:
#         model = Alternativa
#         fields = ['question', 'text', 'correct']
#         widgets = {
#         'question': forms.HiddenInput(),        
#         }


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.fields['question'].required = False
#         self.fields['text'].required = True
#         self.fields['correct'].required = False
#         self.fields['text'] = SummernoteTextFormField(required = True)
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.fields['body'] = SummernoteTextFormField(required = True)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.fields['body'] = SummernoteTextFormField(required = True)
        
class SolucaoForm(forms.ModelForm):
    class Meta:
        model = Solucao
        fields = ['autor', 'questao', 'bodysol'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questao'].required = False
        self.fields['autor'].required = False       
        
        self.fields['bodysol'] = SummernoteTextFormField(required = False)
        
