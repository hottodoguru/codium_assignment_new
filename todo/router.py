from rest_framework import routers
from .viewsets import TodoViewSet

app_name= "todo"

router = routers.DefaultRouter()
router.register('todo',TodoViewSet)