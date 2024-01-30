from django.db import models
from django.conf import settings
from autoslug import AutoSlugField

class Espaco(models.Model):
    """Espaco object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    
    title = models.CharField(max_length=45, unique=True)
    description = models.TextField(max_length=160, blank=True)
    
    slug = AutoSlugField(unique=True, populate_from='title')   
    
    def __str__(self):
        return self.title 
      
    
class Tag(models.Model):
    """Espaco object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=45, unique=False)  
    
    category = models.CharField(max_length=255)  
    
    def __str__(self):
        return self.name
    
class Questao(models.Model):    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=255)
    body = models.TextField()
    current_answer = models.TextField()
    times_solved = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    
    
class Alternativa(models.Model):
    question = models.ForeignKey(
        Questao, 
        on_delete=models.CASCADE)
    text = models.TextField()  
    correct = models.BooleanField(default=False)
    
    