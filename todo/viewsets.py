from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime

from openpyxl import Workbook
from rest_framework import viewsets, status,permissions, filters, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from todo.models import Todo, Log
from todo.serializers import TodoSerializer, UserSerializer, TodoSerializerNotAuthenticated, LogSerializer
from todo.permission import TodoPermission, IsOwnerOrReadOnly
from todo.functions import export_to_excel



class TodoViewSet(viewsets.ModelViewSet):
        
    queryset = Todo.objects.all()

    #Check if users are authenticated if not only name can read
    def get_serializer_class(self):
        if self.request.user.is_authenticated: 
            return TodoSerializer
        return TodoSerializerNotAuthenticated

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter , DjangoFilterBackend]
    
    ordering_fields = ('name', )
    ordering = ('name', )
    
    search_fields = ('$name', )
    
    filterset_fields = ('status', )

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['owner'] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        todo = get_object_or_404(Todo, name= data['name'])
        log = Log(
                user=request.user,
                name_log = data['name'],
                action=f'Created object: ' + str(data['name']),
                timestamp=datetime.now(),
            )
        log.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        old_name = instance.name
        self.perform_update(serializer)
        data = serializer.validated_data

        headers = self.get_success_headers(serializer.data)

        todo = get_object_or_404(Todo, name= data['name'])
        log = Log(
                user=request.user,
                name_log = old_name,
                action=f'Update object: ' + str(data['name']),
                timestamp=datetime.now(),
            )
        log.save()

        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        log = Log(
                user=request.user,
                name_log = instance.name,
                action=f'Deleted object: ' + str(instance.name),
                timestamp=datetime.now(),
            )
        log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def export_to_excel(self, request, *args, **kwargs):

        export_function = export_to_excel(self,request)

        return export_function


class LogListView(generics.ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)