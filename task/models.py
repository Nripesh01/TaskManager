from django.contrib.auth.models import User
from django.db import models

# your app is purely a JSON-based API.
# Backend only: Django + DRF handles everything.
# API endpoints accept JSON requests and return JSON responses.
# No frontend is needed — tools like Postman, curl, or a mobile app can interact with your API.
# Authentication is handled via JWT tokens.


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    # models.CASCADE → Delete the task if the user is deleted.
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    # on_delete=models.SET_NULL means:
           # : “If the referenced Category is deleted, set this field (category) to NULL instead of deleting the Task.”
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title