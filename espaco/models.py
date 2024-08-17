from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.functions import Lower


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
    """Espaco object."""
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
    name_normalized = models.CharField(max_length=255, editable=False, default='')

    class Meta:
        ordering = ['name_normalized']
        
    def save(self, *args, **kwargs):
        self.name_normalized = self._normalize_name()
        super().save(*args, **kwargs)
        
    def _normalize_name(self):
        return self.name.lower()
    
    
    