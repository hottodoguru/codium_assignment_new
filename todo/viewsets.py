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
from todo.serializers import TodoSerializer, UserSerializer, LogSerializer
from todo.permission import IsOwnerOrReadOnly
from todo.functions import export_to_excel



class TodoViewSet(viewsets.ModelViewSet):
        
    queryset = Todo.objects.all()

    # Check if users are authenticated if not only name can read
    def get_serializer_class(self):
        return TodoSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter , DjangoFilterBackend]
    
    ordering_fields = ('name', )
    ordering = ('name', )
    
    search_fields = ('$name', )
    
    filterset_fields = ('status', )

    
    def perform_destroy(self, instance):
        log = Log(
                user=instance.owner,
                name_log = instance.name,
                action=f'Deleted object: ' + str(instance.name),
                timestamp=datetime.now(),
            )
        log.save()
        super().perform_destroy
    
    def export_to_excel(self, request, *args, **kwargs):

        export_workbook = export_to_excel(self,request)
        
        file_name = 'todo_export.xlsx'
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # Create response object with file attachment
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        # Save workbook to response
        export_workbook.save(response)

        return response


class LogListView(generics.ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)