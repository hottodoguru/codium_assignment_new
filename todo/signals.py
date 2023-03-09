from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Todo


#@receiver(pre_save, sender= Todo)
#def create_todo(sender, request, *args, **kwargs):
#    Todo.objects.create(name = sender.name,description = sender.description, status = sender.status ,owner=request.user)

@receiver(post_save, sender= Todo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance.name)