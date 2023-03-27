from rest_framework import routers
from todo.viewsets import TodoViewSet, LogListView

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from todo.views import LoginView

app_name= "todo"

router = routers.DefaultRouter()
router.register('todo',TodoViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('log/', LogListView.as_view(), name='log'),
]
urlpatterns += router.urls