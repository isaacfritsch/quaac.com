from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from espaco.models import Espaco, Tag

class Questao(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
    )
    body = models.TextField()    
    times_solved = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)


# class Alternativa(models.Model):
#     question = models.ForeignKey(
#         Questao,
#         on_delete=models.CASCADE)
#     text = models.TextField()
#     correct = models.BooleanField(default=False)
    
class Comment(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    body = models.TextField()
    data = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        try:
            return f'{self.autor.name} : {self.body[:30]}' 
        except:
            return f'no author : {self.body[:30]}' 
        
    class Meta:
        ordering = ['-data']

class Reply(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor} - {self.body[:20]}'
        
    
class Solucao(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    bodysol = models.TextField()
    data = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        try:
            return f'{self.autor.name} : {self.bodysol[:30]}' 
        except:
            return f'no author : {self.bodysol[:30]}' 
        
    class Meta:
        ordering = ['-data']
        

