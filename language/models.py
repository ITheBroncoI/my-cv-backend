from django.db import models
from django.conf import settings

# Create your models here.
class Language(models.Model):
    language   = models.TextField(default='')
    posted_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)