from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
# Create your models here.
 


    
    
User = settings.AUTH_USER_MODEL


class Todo(models.Model):
    class Status(models.TextChoices):
        not_done = "1", "Not Done"
        doing = "2", "Doing"
        done = "3", "Done"
    
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length = 20, choices=Status.choices, default=Status.not_done)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)



class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_log = models.CharField(max_length = 200, null=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add = True)