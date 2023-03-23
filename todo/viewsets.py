from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from todo.functions import export_to_excel
from todo.models import Todo, Log
from todo.permission import IsOwnerOrReadOnly
from todo.serializers import TodoSerializer, UserSerializer, LogSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()

    # Check if users are authenticated if not only name can read
    def get_serializer_class(self):
        return TodoSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]

    ordering_fields = ('name',)
    ordering = ('name',)

    search_fields = ('$name',)

    filterset_fields = ('status',)

    def perform_destroy(self, instance):
        log = Log(
            user=instance.owner,
            name_log=instance.name,
            action=f'Deleted object: ' + str(instance.name),
            timestamp=datetime.now(),
        )
        log.save()
        super().perform_destroy()

    @action(detail=False, methods=['GET'])
    def export_excel(self, request, *args, **kwargs):
        exported_workbook = export_to_excel(self, request)

        file_name = 'todo_export.xlsx'
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # Create response object with file attachment
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        # Save workbook to response
        exported_workbook.save(response)

        return response


class LogListView(generics.ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
