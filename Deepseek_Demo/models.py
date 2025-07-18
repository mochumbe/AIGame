# models.py
from django.db import models
from django.contrib.auth.models import User

class DeepSeekAPIKey(models.Model):
    api_key = models.CharField(max_length=128)
    last_used = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"API Key for {self.api_key} (Active: {self.is_active})"

class Conversation(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    user_message = models.TextField()
    ai_response = models.TextField()
    course_context = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Conversation at {self.timestamp} - Context: {self.course_context or 'No context'}"