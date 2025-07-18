from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, DeepSeekAPIKey
from .services.deepseek_services import DeepSeekAI
import json
import requests


def index(request):
    return render(request, 'index.html')
@csrf_exempt
def ai_chat(request):
    import logging
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')


        # Fetch the first active API key (global key)
        try:
            api_key_obj = DeepSeekAPIKey.objects.filter(is_active=True).first()
            if not api_key_obj:
                logging.error("No active DeepSeek API key found.")
                return JsonResponse({'response': 'No active DeepSeek API key found.'})
            api_key = api_key_obj.api_key
        except Exception as e:
            logging.exception("Error fetching DeepSeek API key:")
            return JsonResponse({'response': 'Error fetching DeepSeek API key.'})

        # Call DeepSeek API
        try:
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": user_message}
                    ]
                }
            )
            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content']
            else:
                logging.error(f"DeepSeek API error: {response.status_code} {response.text}")
                ai_response = "Sorry, there was an error contacting the AI."
        except Exception as e:
            logging.exception("Exception when calling DeepSeek API:")
            ai_response = "Sorry, there was an error contacting the AI."

        return JsonResponse({'response': ai_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)