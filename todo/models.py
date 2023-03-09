from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
 


    
    
User = settings.AUTH_USER_MODEL


class Todo(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True)

