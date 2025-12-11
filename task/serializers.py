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
from .models import Task, Category



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']
        # read_only_fields = ['user']: This tells DRF not to expect the 'user' field from the client (so the client cannot change it).
        # The field is read-only in the API.
        
# in views.py,  
# serializer.save(user=request.user):
   # Even though 'user' is read-only, you can still set it manually in the backend.
   # DRF will take request.user (the currently logged-in user) and assign it to the 'user' field of the Task when saving.
   # This ensures that the task always belongs to the logged-in user, even if the client doesn’t send a user field.
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



#TaskSerializer:
# Converts the Task model into JSON so it can be sent to clients.

# Also allows incoming JSON data to be converted into Python objects and saved to the database.

# Purpose: Bridges Python models ↔ JSON for your API.


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # ensures password is never sent back in API responses.
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
    def create(self, validated_data):
        user = User.objects.create_user(         # create() method properly hashes password using User.objects.create_user().
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['id', 'username', 'password', 'is_staff']