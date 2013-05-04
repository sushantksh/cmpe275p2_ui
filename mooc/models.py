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
    
    def get_primary_url(self):
        return self.primary_URL
        
    def get_secondary_url(self):
        return self.secondary_URL

	def is_default_group(self):
	    return self.is_default