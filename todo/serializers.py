from .models import Todo
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


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


#class LoginSerializer(serializers.Serializer):
#    username = serializers.CharField()
#    password = serializers.CharField()
#
#    def validate(self, data):
#        user = authenticate(username=data['username'], password=data['password'])
#        if user and user.is_active:
#            refresh = RefreshToken.for_user(user)
#            return {
#                'user': user,
#                'refresh': str(refresh),
#                'access': str(refresh.access_token),
#            }
#        raise serializers.ValidationError('Incorrect credentials')






class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['name', 'description', 'status','owner','date']
        extra_kwargs = {
                        'owner': {'read_only': True}
                    }
    def to_representation(self, instance):
        user = self.context['request'].user
        if user.is_authenticated and instance.owner == user :
            return super().to_representation(instance)
        else:
            return {'name' : instance.name}

class TodoSerializerNotAuthenticated(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['name']
        
