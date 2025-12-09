from django.contrib.auth.models import User
from django.db import models

# your app is purely a JSON-based API.
# Backend only: Django + DRF handles everything.
# API endpoints accept JSON requests and return JSON responses.
# No frontend is needed — tools like Postman, curl, or a mobile app can interact with your API.
# Authentication is handled via JWT tokens.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title