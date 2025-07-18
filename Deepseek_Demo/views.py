from django.shortcuts import render

# Create your views here.
# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation
from .services.deepseek_services import DeepSeekAI
import json

@login_required
@csrf_exempt  # Only for development, use proper CSRF in production
def ask_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')
            context = data.get('context')
            
            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)
            
            response, error = DeepSeekAI.ask_question(request.user, question, context)
            
            if error:
                return JsonResponse({'error': error}, status=500)
            
            # Save conversation
            Conversation.objects.create(
                user=request.user,
                user_message=question,
                ai_response=response,
                course_context=context
            )
            
            return JsonResponse({'response': response})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def get_conversation_history(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-timestamp')[:10]
    data = [{
        'timestamp': conv.timestamp.strftime("%Y-%m-%d %H:%M"),
        'user_message': conv.user_message,
        'ai_response': conv.ai_response,
        'context': conv.course_context
    } for conv in conversations]
    return JsonResponse({'conversations': data})

def index(request):
    """
    Render the home page.
    """
    return render(request, 'index.html')