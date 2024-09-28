from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from espaco.models import Espaco, Tag
from users.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        
class Questao(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
    )
    body = models.TextField()    
    times_solved = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    likes = GenericRelation(Like)
      

    
class Comment(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    body = models.TextField()
    data = models.DateTimeField(auto_now_add=True) 
    likes = GenericRelation(Like)

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
    likes = GenericRelation(Like)

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
    likes = GenericRelation(Like)   

    def __str__(self):
        try:
            return f'{self.autor.name} : {self.bodysol[:30]}' 
        except:
            return f'no author : {self.bodysol[:30]}' 
        
    class Meta:
        ordering = ['-data']
        
class Replysolucao(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True
    )
    solucao = models.ForeignKey(Solucao, on_delete=models.CASCADE, related_name='replies_solucao')
    body = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return f'{self.autor} - {self.body[:20]}'
    
class Resolucao(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    questao = models.ForeignKey(
        'Questao',
        on_delete=models.CASCADE,
    )
    resolvida = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'questao')


 
    

        

