from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.functions import Lower
import re

def natural_key(string):
    # Função que separa a string em partes de texto e números
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', string)]

class TagQuerySet(models.QuerySet):
    def natural_ordering(self):
        return sorted(self, key=lambda tag: natural_key(tag.name))
    
class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def natural_ordering(self):
        return self.get_queryset().natural_ordering()
    
class Espaco(models.Model):
    """Espaco object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    title = models.CharField(max_length=45, unique=True)
    description = models.TextField(max_length=255, blank=True)
    
    slug = AutoSlugField(unique=True, populate_from='title')   
    
    def __str__(self):
        return self.title
      
   
class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(max_length=45, unique=False)  
    category = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)    

    objects = TagManager()

    def __str__(self):
        return self.name

    