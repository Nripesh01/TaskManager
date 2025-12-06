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

#TaskSerializer:
# Converts the Task model into JSON so it can be sent to clients.

# Also allows incoming JSON data to be converted into Python objects and saved to the database.

# Purpose: Bridges Python models ↔ JSON for your API.