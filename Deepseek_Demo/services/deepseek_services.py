# services/deepseek_service.py
import requests
from django.conf import settings
from django.contrib.auth.models import User
from Deepseek_Demo.models import DeepSeekAPIKey

class DeepSeekAI:
    API_URL = "https://api.deepseek.com/v1/chat/completions"  # Update with actual API URL
    
    @classmethod
    def get_api_key(cls, user):
        try:
            return DeepSeekAPIKey.objects.get(user=user).api_key
        except DeepSeekAPIKey.DoesNotExist:
            return None
    
    @classmethod
    def ask_question(cls, user, question, context=None):
        api_key = cls.get_api_key(user)
        if not api_key:
            return None, "No API key configured for this user"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",  # Update with correct model name
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a helpful study assistant for university students. {f'Current course context: {context}' if context else ''}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(cls.API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'], None
        except requests.exceptions.RequestException as e:
            return None, str(e)