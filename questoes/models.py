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
    current_answer = models.TextField(default=None, blank=True)
    times_solved = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)


class Alternativa(models.Model):
    question = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)
