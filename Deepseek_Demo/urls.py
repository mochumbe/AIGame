from django.urls import path
from . import views
from .views import ask_ai, get_conversation_history

urlpatterns = [
    path('', views.index, name='index'),  # Home page view
    path('api/ask-ai/', ask_ai, name='ask_ai'),
    path('api/conversation-history/', get_conversation_history, name='conversation_history')
    ]