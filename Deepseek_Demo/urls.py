from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Home page view

    path('ai-chat/', views.ai_chat, name='ai_chat'),
    ]