from .models import Todo
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {
                'validators': [
                    validators.UniqueValidator(queryset=User.objects.all())
                ]
            },
            'email': {
                'validators': [
                    validators.UniqueValidator(queryset=User.objects.all())
                ]
            },
            'password': {
                'write_only': True
            }
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for returning JWT token"""
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # add extra responses
        data['user'] = UserSerializer(self.user).data

        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'user': user,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError('Incorrect credentials')






class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['name', 'description', 'status','owner']
        extra_kwargs = {
                        'owner': {'read_only': True}
                    }
        


