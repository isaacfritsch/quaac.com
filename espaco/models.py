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
    description = models.TextField(max_length=255, blank=True)
    
    slug = AutoSlugField(unique=True, populate_from='title')   
    
    def __str__(self):
        return self.title
      
   
class Tag(models.Model):
    """Espaco object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null = False
    )
    space = models.ForeignKey(
        Espaco,
        on_delete=models.CASCADE,
        null = False
    )
    name = models.CharField(max_length=45, unique=False)  
    
    category = models.CharField(max_length=255)  
    
    def __str__(self):
        return self.name
    

    
    