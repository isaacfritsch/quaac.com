from django.contrib import admin
from questoes import models
from django_summernote.admin import SummernoteModelAdmin


class QuestaoAdmin(SummernoteModelAdmin):
    summernote_fields = ('body','current_answer',)   

    
class ComentarioAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    
class SolucaoAdmin(SummernoteModelAdmin):
    summernote_fields = ('bodysol',)
    
class ReplyAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    
class ReplysolucaoAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)


admin.site.register(models.Questao, QuestaoAdmin,)
admin.site.register(models.Comment, ComentarioAdmin,)
admin.site.register(models.Solucao, SolucaoAdmin,)
admin.site.register(models.Reply, ReplyAdmin,)
admin.site.register(models.Replysolucao, ReplysolucaoAdmin,)



