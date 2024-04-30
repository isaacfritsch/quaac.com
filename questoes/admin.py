from django.contrib import admin
from questoes import models
from django_summernote.admin import SummernoteModelAdmin


class QuestaoAdmin(SummernoteModelAdmin):
    summernote_fields = ('body','current_answer',)
    
class AlternativaAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)
    
class ComentarioAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    
class SolucaoAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

admin.site.register( models.Alternativa, AlternativaAdmin)
admin.site.register(models.Questao, QuestaoAdmin,)
admin.site.register(models.Comment, ComentarioAdmin,)
admin.site.register(models.Solucao, SolucaoAdmin,)



