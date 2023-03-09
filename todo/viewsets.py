from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer

from django.contrib.auth import authenticate

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication


class TodoViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    user = authenticate()
    
    @api_view(['POST'])
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['owner'] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)