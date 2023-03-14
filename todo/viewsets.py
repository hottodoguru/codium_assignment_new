from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer, UserSerializer, TodoSerializerNotAuthenticated

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets, status,permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from todo import serializers



class TodoViewSet(viewsets.ModelViewSet):
        
    queryset = Todo.objects.all()

    #Check if users are authenticated if not only name can read
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            serializer_class = TodoSerializer
            return serializer_class
        else:
            serializer_class = TodoSerializerNotAuthenticated
            return serializer_class

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter , DjangoFilterBackend]
    
    ordering_fields = ['name']
    ordering = ['name']
    
    search_fields = ['$name']
    #filterset_fields = {
    #    'name' : ['icontains'],
    #    }
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['owner'] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    



    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)