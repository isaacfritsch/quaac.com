from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from espaco.models import Espaco, Tag
from ckeditor.fields import RichTextField

class Questao(models.Model):    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
    )
    body = RichTextField()
    current_answer = RichTextField(default=None, blank=True)
    times_solved = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    
    
class Alternativa(models.Model):
    question = models.ForeignKey(
        Questao, 
        on_delete=models.CASCADE)
    text = RichTextField()
    correct = models.BooleanField(default=False)
