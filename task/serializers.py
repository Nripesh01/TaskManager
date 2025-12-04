# We use a serializer in Django REST Framework (DRF) because it acts as a bridge between Python objects 
# (like Django models) and JSON, which is the standard format for APIs
# User is the built-in Django user model.
# Fields it includes by default:
# username
# email
# password (hashed)
# first_name, last_name
# is_staff, is_superuser, is_active


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
# write_only=True is The password will only be used when creating/updating a user. 
# required=True This ensures that the password field cannot be empty during registration.
# style is the custom used to show in browsable API
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
    def create(self, validated_data): # validated_data is the dictionary of user input that is already safe.
        user = User.objects.create_user(
            username=validated_data['username'], # validated_data['username'] = taking the username from that dictionary.
            password=validated_data['password'],
            emial=validated_data.get['email']
        )
        return user