from django.db import models

# Create your models here.
class MOOC(models.Model):
    group = models.CharField(max_length=256)
    primary_URL = models.CharField(max_length=512)
    secondary_URL = models.CharField(max_length=512)
    is_default = models.BooleanField(default=False)
    
    # Python 3: def __str__(self):     
    def __unicode__(self):  
       return self.group
