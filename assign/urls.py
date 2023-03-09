"""assign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.urls import path,include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from todo.views import LoginView
from todo import router as todo_api_router

router = DefaultRouter()
app_name = 'api_urls'



urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/', include(todo_api_router.router.urls)),
    path('backend/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/api/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('backend/api/login/', LoginView.as_view(), name='login'),
    #path(r'todolist/',include(todo_api_router.router.urls)),
]
urlpatterns += router.urls